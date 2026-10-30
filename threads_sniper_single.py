"""
Single Thread Sniper Engine.
Allows direct targeting of any specific Threads URL on demand.
Extracts post context, runs OpenRouter/Never-Lie evaluation, and drafts custom 4-part replies.
"""

import os
import sys
import json
import time
import re
from playwright.sync_api import sync_playwright

import reply_generator
import db
import reply_automation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "threads_session.json")

def analyze_thread_url(thread_url: str):
    """
    Loads a single thread URL via Playwright, extracts post text,
    and runs the Never-Lie evaluator.
    """
    clean_url = thread_url.strip().split("?")[0]
    
    # Try extracting author from URL if formatted like https://www.threads.net/@user/post/xxx
    author_match = re.search(r'@([a-zA-Z0-9_\.]+)', clean_url)
    author_guess = author_match.group(1) if author_match else "user"

    post_text = ""
    author = author_guess

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )

            if os.path.exists(SESSION_PATH):
                with open(SESSION_PATH, "r") as f:
                    session_data = json.load(f)
                context.add_cookies(session_data.get("cookies", []))

            page = context.new_page()
            page.goto(clean_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(2500)

            # Extract first article / post body
            articles = page.locator("article")
            if articles.count() > 0:
                post_text = articles.first.inner_text().strip()
                author_el = articles.first.locator("a[href^='/@']").first
                if author_el.count() > 0:
                    href = author_el.get_attribute("href") or ""
                    author = href.lstrip("/@").split("/")[0] or author
            else:
                # Fallback to main content
                post_text = page.locator("main").inner_text().strip()

            browser.close()
    except Exception as e:
        print(f"Error scraping single thread {clean_url}: {e}")
        return {
            "status": "error",
            "message": f"Failed to load thread page: {e}"
        }

    if not post_text or len(post_text) < 15:
        return {
            "status": "error",
            "message": "Could not extract thread content. The post may be private or deleted."
        }

    # Evaluate with reply_generator
    eval_res = reply_generator.evaluate_and_draft(post_text, author=author)

    return {
        "status": "ok",
        "url": clean_url,
        "author": author,
        "thread_text": post_text[:600],
        "evaluation": eval_res
    }

def dispatch_quick_snipe(thread_url: str, reply_text: str, slot: int, author: str, thread_text: str = ""):
    """
    Directly dispatches a custom reply to the specified thread URL
    and records it in the database.
    """
    clean_url = thread_url.strip().split("?")[0]
    spec = reply_generator.CATALOG_SPECS.get(slot, {})
    prod_name = spec.get("name", f"Product #{slot}")

    # Add to queue as dispatching
    queue_id = db.add_to_queue(
        ip_id="emma",
        author=author,
        thread_url=clean_url,
        thread_text=thread_text or "Quick Sniper Dispatched Post",
        slot=slot,
        product_name=prod_name,
        draft_reply=reply_text,
        engagement_tier="⚡ QUICK SNIPER",
        likes_count=100,
        replies_count=10,
        opportunity_score=100
    )

    if not queue_id:
        # Check if already in queue
        conn = db.get_connection()
        c = conn.cursor()
        row = c.execute("SELECT id FROM reply_approval_queue WHERE thread_url = ?", (clean_url,)).fetchone()
        conn.close()
        queue_id = row[0] if row else None

    if queue_id:
        db.update_queue_status(queue_id, "dispatching")
        success = reply_automation.send_approved_reply(queue_id)
        return {
            "status": "ok" if success else "failed",
            "queue_id": queue_id
        }
    else:
        return {
            "status": "error",
            "message": "Failed to create queue entry for dispatch"
        }
