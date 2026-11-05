"""
Indonesian Threads Sniffer & Lead Scorer for NemuAja Shopee Affiliate Engine (Fase 3).
Scrapes Indonesian Threads queries, matches problem solvers dynamically, and queues high-converting leads under ip_id='nemuaja'.
"""

import os
import sys
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import db
import nemuaja_generator
from threads_sniffer import extract_posts_from_graphql

SESSION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threads_session.json")

# High-intent Indonesian pain point queries
INDONESIAN_QUERIES = [
    # Core Evergreen
    "wajan gosong kerak",
    "panci gosong bersihin",
    "kamar mandi kosan sempit",
    "rak tempel tanpa bor",
    "males ngepel lantai",
    "ketiak bau asem",
    "deodorant bikin kuning",
    "jerawat batu sakit",
    "jerawat mendem",
    # Dynamic Phase 3 Queries (Household, Pets, Hygiene)
    "kucing pipis sembarangan",
    "bau pesing kucing kasur",
    "kipas angin kotor debu",
    "sepatu putih dekil",
    "kabel charger gampang rusak",
    "baju kemeja lecek setrika"
]

def stream_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [NemuAja-Indo] {msg}")
    sys.stdout.flush()

def run_sniffer_indo(max_queries=3, headless=True):
    pending_count = db.get_pending_queue_count("nemuaja")
    if pending_count >= 50:
        stream_log(f"🛑 Smart Queue Cap: Queue already has {pending_count} pending leads for NemuAja Indo. Skipping scrape.")
        return 0

    if not os.path.exists(SESSION_PATH):
        stream_log("❌ threads_session.json not found!")
        return 0

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    conn = db.get_connection()
    c = conn.cursor()

    total_added = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        context.add_cookies(cookies)
        page = context.new_page()

        extracted_posts = []

        def handle_response(response):
            url = response.url
            if "graphql" in url or "api/graphql" in url:
                try:
                    ct = response.headers.get("content-type", "")
                    if "application/json" in ct and response.status == 200:
                        posts = extract_posts_from_graphql(response.json())
                        if posts:
                            for p in posts:
                                extracted_posts.append({
                                    "text": p["text"],
                                    "author": p["username"],
                                    "url": p["url"],
                                    "likes": p["like_count"],
                                    "replies": p["reply_count"]
                                })
                except Exception:
                    pass

        page.on("response", handle_response)

        for query in INDONESIAN_QUERIES[:max_queries]:
            encoded_q = query.replace(" ", "%20")
            search_url = f"https://www.threads.net/search?q={encoded_q}&serp_type=default&filter=recent"
            stream_log(f"🔍 Searching Threads: '{query}'...")

            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3500)

                # Scroll down 2 times to trigger GraphQL feed
                for _ in range(2):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)

                stream_log(f"   Extracted {len(extracted_posts)} posts from search.")

                for post in extracted_posts:
                    text = post["text"]
                    author = post["author"]
                    post_url = post["url"]
                    likes = post["likes"]
                    replies = post["replies"]

                    if not post_url or not author:
                        continue

                    # Check duplicate
                    c.execute("SELECT id FROM reply_approval_queue WHERE ip_id = 'nemuaja' AND thread_url = ?", (post_url,))
                    if c.fetchone():
                        continue

                    # Pre-screen
                    ok, reason = nemuaja_generator.pre_screen_indo(text, author)
                    if not ok:
                        continue

                    # Contextual LLM evaluation and reply drafting
                    eval_res = nemuaja_generator.generate_reply_indo_llm(text, author=author)
                    if not eval_res or eval_res.get("verdict") != "ACCEPT":
                        continue

                    slug = eval_res.get("slug", "solusi")
                    prod_name = eval_res.get("product_name", "Solusi Shopee")
                    draft = eval_res.get("reply_text", "")

                    if not draft:
                        continue

                    tier = "🔥 VIRAL HIJACK" if (likes >= 15 or replies >= 5) else "⚡ FRESH SNIPER"
                    score = min(100, 60 + (likes * 2) + (replies * 3))

                    db.add_to_queue(
                        ip_id="nemuaja",
                        author=author,
                        thread_url=post_url,
                        thread_text=text,
                        slot=0,
                        product_name=f"Shopee: {prod_name} ({slug})",
                        draft_reply=draft,
                        likes_count=likes,
                        replies_count=replies,
                        engagement_tier=tier,
                        opportunity_score=score
                    )
                    stream_log(f"✅ [nemuaja] Added lead for @{author}: {prod_name} ({tier} | Score: {score})")
                    total_added += 1

                extracted_posts.clear()

            except Exception as e:
                stream_log(f"⚠️ Error searching '{query}': {e}")

        conn.close()
        browser.close()

    stream_log(f"🎉 NemuAja Sniffer finished. Added {total_added} new leads.")
    return total_added

if __name__ == "__main__":
    run_sniffer_indo(max_queries=2, headless=True)
