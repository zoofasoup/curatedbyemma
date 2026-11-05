"""
Indonesian Threads Sniffer & Lead Scorer for NemuAja Shopee Affiliate Engine (Fase 3 Dynamic).
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
    "wajan gosong",
    "panci gosong",
    "kamar mandi kosan",
    "rak tanpa bor",
    "males ngepel",
    "ketiak bau asem",
    "deodorant bikin kuning",
    "jerawat batu",
    "jerawat mendem",
    "kucing pipis sembarangan",
    "bau pesing kasur",
    "kipas angin berdebu",
    "sepatu putih dekil",
    "kabel charger rusak"
]

def stream_log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [NemuAja-Indo] {msg}")
    sys.stdout.flush()

def run_sniffer_indo(max_queries=2, scrolls=2, headless=True):
    pending_count = db.get_pending_queue_count("nemuaja")
    if pending_count >= 50:
        stream_log(f"🛑 Smart Queue Cap: NemuAja queue already has {pending_count} pending leads. Skipping scrape.")
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
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-ipv6']
        )
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        intercepted_raw_posts = []

        def on_response(response):
            url = response.url
            if "graphql" in url or "api/graphql" in url:
                try:
                    ct = response.headers.get("content-type", "")
                    if "application/json" in ct and response.status == 200:
                        posts = extract_posts_from_graphql(response.json())
                        if posts:
                            intercepted_raw_posts.extend(posts)
                except Exception:
                    pass

        page.on("response", on_response)

        for query in INDONESIAN_QUERIES[:max_queries]:
            encoded_q = query.replace(" ", "%20")
            search_url = f"https://www.threads.net/search?q={encoded_q}&serp_type=default"
            stream_log(f"🔍 Searching Threads: '{query}' ({search_url})...")

            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(2500)

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

                # 2. Scroll with mouse wheel to trigger GraphQL
                for _ in range(scrolls):
                    page.mouse.wheel(0, 3000)
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
                            if u_name and u_name not in ("curated_byemma", "nemuaja") and len(art_text) > 30:
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
                stream_log(f"⚠️ Error scraping '{query}': {e}")

        browser.close()

    # Deduplicate by URL or Text
    unique_posts = {}
    for p in intercepted_raw_posts:
        uid = p.get("url") or str(abs(hash(p.get("text", ""))))
        unique_posts[uid] = p

    stream_log(f"✅ Scraping done. Found {len(unique_posts)} unique candidate posts. Evaluating with AI...")

    for uid, post in list(unique_posts.items())[:15]:
        text = post.get("text", "")
        author = post.get("username", "user")
        post_url = post.get("url", "")
        likes = post.get("like_count", 0)
        replies = post.get("reply_count", 0)

        if not post_url or not text or len(text.strip()) < 20:
            continue

        # Check duplicate
        c.execute("SELECT id FROM reply_approval_queue WHERE ip_id = 'nemuaja' AND thread_url = ?", (post_url,))
        if c.fetchone():
            continue

        # Rule Pre-screen
        ok, reason = nemuaja_generator.pre_screen_indo(text, author)
        if not ok:
            continue

        # AI Evaluation & Reply Drafting
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

    conn.close()
    stream_log(f"🎉 NemuAja Sniffer finished. Added {total_added} new leads.")
    return total_added

if __name__ == "__main__":
    run_sniffer_indo(max_queries=2, scrolls=2, headless=True)
