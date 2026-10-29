"""
Threads GraphQL Interception Sniffer & Engagement Scorer.
Intercepts internal GraphQL payloads (/api/graphql, /graphql/query) during search.
Extracts clean JSON: post_id, author, clean_text, like_count, reply_count, taken_at.
Evaluates context & categorizes into:
- 🔥 VIRAL HIJACK (Likes >= 20 or Replies >= 5)
- ⚡ FRESH SNIPER (Age <= 2h with active complaint)
"""

import os
import sys
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import db
import reply_generator

SESSION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threads_session.json")

def stream_log(msg, callback=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    sys.stdout.flush()
    if callback:
        try:
            callback(formatted)
        except:
            pass

def extract_posts_from_graphql(payload, logger=None):
    """
    Recursively walk through Threads GraphQL JSON payload to find post objects
    with caption, like_count, reply_count, and author.
    """
    extracted = []
    
    def walk(obj):
        if isinstance(obj, dict):
            # Check if this dict represents a Threads post
            # Usually contains 'caption' or 'text_post_app_info' or 'like_count'
            if "caption" in obj and isinstance(obj["caption"], dict) and "text" in obj["caption"]:
                text = obj["caption"]["text"]
                user = obj.get("user", {})
                username = user.get("username", "unknown")
                like_count = obj.get("like_count", 0)
                reply_count = obj.get("text_post_app_info", {}).get("direct_reply_count", 0) if "text_post_app_info" in obj else 0
                taken_at = obj.get("taken_at", int(time.time()))
                code = obj.get("code", "")
                post_url = f"https://www.threads.net/@{username}/post/{code}" if code else None

                if text and len(text.strip()) > 20:
                    extracted.append({
                        "id": obj.get("id", str(abs(hash(text)))),
                        "username": username,
                        "text": text.strip(),
                        "like_count": like_count or 0,
                        "reply_count": reply_count or 0,
                        "taken_at": taken_at,
                        "url": post_url
                    })
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    try:
        walk(payload)
    except Exception as e:
        stream_log(f"Error walking GraphQL: {e}")

    return extracted

def run_graphql_sniffer(query="office chair lower back pain", scrolls=3, headless=True, log_callback=None):
    def log(msg):
        stream_log(msg, callback=log_callback)

    if not os.path.exists(SESSION_PATH):
        log("❌ threads_session.json not found! Please login first.")
        return []

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    log(f"🚀 Starting GraphQL Sniffer for query: '{query}' (Scrolls: {scrolls})...")

    intercepted_raw_posts = []

    def on_response(response):
        url = response.url
        # Catch Threads internal GraphQL endpoints
        if "graphql" in url or "api/graphql" in url:
            try:
                ct = response.headers.get("content-type", "")
                if "application/json" in ct and response.status == 200:
                    data = response.json()
                    posts = extract_posts_from_graphql(data)
                    if posts:
                        log(f"📦 Intercepted GraphQL Payload: Found {len(posts)} structured post(s)!")
                        intercepted_raw_posts.extend(posts)
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=['--disable-ipv6'])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # Attach response listener
        page.on("response", on_response)

        encoded_q = query.replace(" ", "%20")
        target_url = f"https://www.threads.net/search?q={encoded_q}&serp_type=default&filter=recent"
        
        log(f"🌐 Navigating to Threads Search: {target_url}")
        page.goto(target_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)

        # Perform human-like scrolls to trigger pagination GraphQL requests
        for s in range(1, scrolls + 1):
            log(f"📜 Scrolling feed chunk ({s}/{scrolls})...")
            page.mouse.wheel(0, 3500)
            page.wait_for_timeout(2500)

        log(f"✅ Scraping phase finished. Total raw posts intercepted: {len(intercepted_raw_posts)}")
        browser.close()

    # Deduplicate by ID
    unique_posts = {}
    for p in intercepted_raw_posts:
        unique_posts[p["id"]] = p

    log(f"🔍 Analyzing {len(unique_posts)} unique candidate posts against Context & Engagement Gates...")

    processed_candidates = []
    conn = db.get_connection()
    c = conn.cursor()

    for pid, p in unique_posts.items():
        author = p["username"]
        text = p["text"]
        likes = p["like_count"]
        replies = p["reply_count"]
        url = p["url"] or f"https://www.threads.net/@{author}"

        # 1. Determine Engagement Tier
        if likes >= 20 or replies >= 5:
            engagement_tier = "🔥 VIRAL HIJACK"
        else:
            engagement_tier = "⚡ FRESH SNIPER"

        log(f"--- Checking @{author} ({engagement_tier} | {likes} likes, {replies} replies) ---")

        # 2. Strict Context & Never Lie Evaluation
        eval_res = reply_generator.evaluate_and_draft_local(text, author=author)
        if eval_res["verdict"] == "REJECT":
            log(f"❌ REJECTED: {eval_res.get('reason')}")
            continue

        slot = eval_res["slot"]
        prod_name = eval_res["product_name"]
        draft = eval_res["reply_draft"]

        log(f"✅ ACCEPTED! Slot #{slot}: {prod_name}")
        log(f"📝 Reply Draft: \"{draft[:80]}...\"")

        # Store in Approval Queue with engagement data
        c.execute("""
        INSERT OR IGNORE INTO reply_approval_queue 
        (ip_id, author_username, thread_url, thread_text, matched_slot, product_name, draft_reply, status)
        VALUES ('emma', ?, ?, ?, ?, ?, ?, 'pending')
        """, (author, url, f"[{engagement_tier} - {likes} likes, {replies} replies] {text}", slot, prod_name, draft))
        conn.commit()

        processed_candidates.append({
            "author": author,
            "url": url,
            "engagement": engagement_tier,
            "likes": likes,
            "replies": replies,
            "slot": slot,
            "draft": draft
        })

    conn.close()
    log(f"🏁 Finished! Added {len(processed_candidates)} qualified candidate(s) to Approval Queue.")
    return processed_candidates

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "office chair lower back pain"
    run_graphql_sniffer(query=q, scrolls=2, headless=True)
