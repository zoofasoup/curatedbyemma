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

SLOT_SEARCH_QUERIES = {
    1: ["dog hair couch", "cat fur sofa", "pet hair blanket", "pet shedding couch"],
    2: ["baby wont sleep", "toddler sleep regression", "baby crying all night"],
    3: ["desk chair back pain", "office chair lumbar", "wfh lower back pain"],
    4: ["air fryer oil", "air fryer soggy", "airfryer greasy"],
    5: ["scrubbing shower tile", "bathroom grout cleaning", "bathtub scrubbing"],
    6: ["charging cables falling", "nightstand cables", "cords falling behind bed"],
    7: ["holding phone flight", "airplane tray phone mount", "plane neck cramp phone"],
    8: ["travel clothes wrinkled", "hotel iron ruined", "steamer travel clothes"],
    9: ["earbuds hurt side sleeping", "sleeping with earbuds", "sleep mask speakers"],
    10: ["car air vent dust", "crumbs car console", "car vent cleaning gel"]
}

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

def run_graphql_sniffer(query="office chair lower back pain", scrolls=2, headless=True, filter_type="both", log_callback=None):
    def log(msg):
        stream_log(msg, callback=log_callback)

    # 0. Smart API Guard: If queue already has 50+ pending leads, stop to conserve OpenRouter API
    pending_count = db.get_pending_queue_count("emma")
    if pending_count >= 50:
        log(f"🛑 Smart Queue Cap: Queue already has {pending_count} pending leads (cap: 50). Skipping scrape & LLM evaluation to conserve API.")
        return []

    if not os.path.exists(SESSION_PATH):
        log("❌ threads_session.json not found! Please login first.")
        return []

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    encoded_q = query.replace(" ", "%20")
    
    # Dual-Search: Top (Viral Hijack with thousands of views) + Recent (Fresh Sniper)
    if filter_type == "top":
        search_targets = [("🔥 TOP / VIRAL", f"https://www.threads.net/search?q={encoded_q}&serp_type=default")]
    elif filter_type == "recent":
        search_targets = [("⚡ RECENT / SNIPER", f"https://www.threads.net/search?q={encoded_q}&serp_type=default&filter=recent")]
    else: # "both"
        search_targets = [
            ("🔥 TOP / VIRAL", f"https://www.threads.net/search?q={encoded_q}&serp_type=default"),
            ("⚡ RECENT / SNIPER", f"https://www.threads.net/search?q={encoded_q}&serp_type=default&filter=recent")
        ]

    log(f"🚀 Starting Sniffer for query: '{query}' ({filter_type.upper()} mode, Scrolls: {scrolls})...")

    intercepted_raw_posts = []

    def on_response(response):
        url = response.url
        if "graphql" in url or "api/graphql" in url:
            try:
                ct = response.headers.get("content-type", "")
                if "application/json" in ct and response.status == 200:
                    data = response.json()
                    posts = extract_posts_from_graphql(data)
                    if posts:
                        intercepted_raw_posts.extend(posts)
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-ipv6'])
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        page.on("response", on_response)

        for label, target_url in search_targets:
            log(f"🌐 Navigating to {label}: {target_url}")
            try:
                page.goto(target_url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(3000)

                # 1. Extract SSR posts from embedded script tags
                try:
                    script_tags = page.locator('script[type="application/json"]').all()
                    for s in script_tags:
                        raw_json = s.inner_text()
                        if "caption" in raw_json or "text_post_app_info" in raw_json:
                            try:
                                parsed_json = json.loads(raw_json)
                                ssr_posts = extract_posts_from_graphql(parsed_json)
                                if ssr_posts:
                                    intercepted_raw_posts.extend(ssr_posts)
                            except Exception:
                                pass
                except Exception:
                    pass

                # 2. Perform scrolls to trigger GraphQL pagination
                for s in range(1, scrolls + 1):
                    page.mouse.wheel(0, 3500)
                    page.wait_for_timeout(2000)

                # 3. Direct DOM fallback
                try:
                    articles = page.locator("article, div[data-pressable-container='true']").all()
                    for art in articles:
                        try:
                            art_text = art.inner_text().strip()
                            if len(art_text) < 25:
                                continue
                            author_link = art.locator("a[href^='/@']").first
                            u_name = author_link.get_attribute("href").lstrip("/@").split("/")[0] if author_link.count() > 0 else ""
                            post_a = art.locator("a[href*='/post/']").first
                            p_href = post_a.get_attribute("href") if post_a.count() > 0 else ""
                            full_p_url = f"https://www.threads.net{p_href}" if p_href.startswith("/") else p_href
                            if u_name and u_name != "curated_byemma" and len(art_text) > 30:
                                intercepted_raw_posts.append({
                                    "id": str(abs(hash(art_text))),
                                    "username": u_name,
                                    "text": art_text,
                                    "like_count": 0,
                                    "reply_count": 0,
                                    "taken_at": int(time.time()),
                                    "url": full_p_url or f"https://www.threads.net/@{u_name}"
                                })
                        except Exception:
                            pass
                except Exception:
                    pass

            except Exception as e:
                log(f"⚠️ Error scraping {label}: {e}")

        log(f"✅ Scraping phase finished. Total raw posts intercepted: {len(intercepted_raw_posts)}")
        browser.close()

    # Deduplicate by ID
    unique_posts = {}
    for p in intercepted_raw_posts:
        unique_posts[p["id"]] = p

    log(f"🔍 Analyzing {len(unique_posts)} unique candidate posts against Context & Engagement Gates...")

    processed_candidates = []

    for pid, p in unique_posts.items():
        author = p["username"]
        text = p["text"]
        likes = p["like_count"]
        replies = p["reply_count"]
        url = p["url"] or f"https://www.threads.net/@{author}"

        # 0. Strict Deduplication Gate
        if db.is_thread_already_processed(url, ip_id="emma"):
            log(f"⏭️ Skipping @{author} ({url}) — already queued or replied.")
            continue

        # 1. Determine Engagement Tier & Opportunity Score
        if likes >= 20 or replies >= 5:
            engagement_tier = "🔥 VIRAL HIJACK"
            opportunity_score = min(100, int(likes + (replies * 3)))
        else:
            engagement_tier = "⚡ FRESH SNIPER"
            opportunity_score = 85 + (15 if replies == 0 else (5 if replies <= 2 else 0))

        log(f"--- Checking @{author} ({engagement_tier} | Score: {opportunity_score} | {likes} likes, {replies} replies) ---")

        # 2. Context & Never Lie Evaluation (OpenRouter LLM with local fallback)
        eval_res = reply_generator.evaluate_and_draft(text, author=author)
        if eval_res["verdict"] == "REJECT":
            log(f"❌ REJECTED: {eval_res.get('reason')}")
            continue

        slot = eval_res["slot"]
        prod_name = eval_res["product_name"]
        draft = eval_res["reply_draft"]
        source = eval_res.get("source", "heuristic")

        log(f"✅ ACCEPTED by {source}! Slot #{slot}: {prod_name}")
        log(f"📝 Reply Draft: \"{draft[:80]}...\"")

        added = db.add_to_queue(
            ip_id="emma",
            author=author,
            thread_url=url,
            thread_text=text,
            slot=slot,
            product_name=prod_name,
            draft_reply=draft,
            engagement_tier=engagement_tier,
            likes_count=likes,
            replies_count=replies,
            opportunity_score=opportunity_score
        )

        if added:
            processed_candidates.append({
                "author": author,
                "url": url,
                "engagement": engagement_tier,
                "score": opportunity_score,
                "likes": likes,
                "replies": replies,
                "slot": slot,
                "draft": draft
            })

    log(f"🏁 Finished! Added {len(processed_candidates)} qualified candidate(s) to Approval Queue.")
    return processed_candidates

def run_query_rotation(slots=None, scrolls=2, headless=True, log_callback=None):
    """
    Rotates queries across the specified slots (default: all 10 slots).
    Picks diverse real-world search phrases so crawler never gets stuck on the same posts.
    """
    target_slots = slots if slots else list(range(1, 11))
    total_found = 0
    for s in target_slots:
        query_candidates = SLOT_SEARCH_QUERIES.get(s, [])
        if isinstance(query_candidates, str):
            query_candidates = [query_candidates]
        # Pick 1-2 search phrases per slot to get broad coverage
        for query in query_candidates[:2]:
            stream_log(f"\n==========================================", callback=log_callback)
            stream_log(f"🎯 SPRINT ROTATOR: Slot #{s} -> Query '{query}'", callback=log_callback)
            stream_log(f"==========================================", callback=log_callback)
            try:
                candidates = run_graphql_sniffer(query=query, scrolls=scrolls, headless=headless, log_callback=log_callback)
                total_found += len(candidates)
                time.sleep(2)
            except Exception as e:
                stream_log(f"⚠️ Error querying slot #{s} ('{query}'): {e}", callback=log_callback)
    return total_found

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--rotate":
        run_query_rotation(scrolls=2, headless=True)
    else:
        q = sys.argv[1] if len(sys.argv) > 1 else "office chair lower back pain"
        run_graphql_sniffer(query=q, scrolls=2, headless=True)
