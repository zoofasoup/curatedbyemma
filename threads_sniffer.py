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
    1: ['dog hair couch', 'cat fur sofa', 'pet shedding couch'],
    2: ['baby wont sleep', 'toddler sleep regression', 'baby crying night'],
    3: ['desk chair back pain', 'office chair lumbar', 'wfh lower back'],
    4: ['air fryer oil', 'air fryer soggy', 'airfryer greasy'],
    5: ['sweater pilling', 'fleece fuzz balls', 'knit cardigan pill'],
    6: ['charging cables falling', 'nightstand cords', 'cables behind bed'],
    7: ['holding phone flight', 'airplane tray mount', 'plane neck cramp phone'],
    8: ['travel clothes wrinkled', 'hotel iron ruined', 'steamer travel clothes'],
    9: ['earbuds hurt side sleeping', 'sleeping with earbuds', 'sleep mask audio'],
    10: ['meat thermometer turkey', 'undercooked chicken', 'dry turkey roast'],
    11: ['shower drain hair clog', 'hair clogging drain', 'tub drain hair snake'],
    12: ['burnt pan bottom', 'scorched skillet grease', 'the pink stuff cleaning'],
    13: ['chomchom roller', 'dog hair furniture', 'cat fur couch removal'],
    14: ['microwave splatter', 'microwave grease baked', 'clean microwave crust'],
    15: ['carpet pet stain', 'couch coffee spill', 'bissell little green'],
    16: ['spilled wine couch', 'couch fabric stain protection', 'scotchgard furniture'],
    17: ['draft under door', 'apartment hallway noise bedroom', 'drafty door winter'],
    18: ['food between stove counter', 'crumbs side of stove', 'stove gap crack'],
    19: ['messy dish soap bottle', 'dish brush sink clutter', 'sink sponge smell'],
    20: ['cant open jar lid', 'stuck pickle jar', 'jar lid vacuum sealed'],
    21: ['hard water ring toilet', 'toilet mineral stains', 'pumice toilet cleaning'],
    22: ['burnt stainless steel pot', 'bar keepers friend stainless', 'heat stains cookware'],
    23: ['smart plug space heater', 'turn off lamp bed', 'smart plug timer'],
    24: ['dropped phone on face bed', 'phone slip hand grip', 'magsafe ring kickstand'],
    25: ['loud upstairs neighbors', 'stomping neighbor ceiling', 'white noise sleep machine'],
    26: ['dehydrated flight', 'dry throat airplane', 'liquid iv travel hydration'],
    27: ['snoring partner earplugs', 'loop earplugs sleep', 'side sleeping earplugs'],
    28: ['frizzy morning hair bedhead', 'satin pillowcase curls', 'sleep creases face'],
    29: ['garbage disposal smell', 'kitchen sink sewer odor', 'stinky disposal blades'],
    30: ['greasy baking sheet soak', 'burnt cheese pan', 'dawn powerwash spray'],
    31: ['clumpy protein powder', 'milk frother wand', 'lumpy matcha powder'],
    32: ['crying chopping onions', 'onion fumes eyes', 'chopping vegetables meal prep'],
    33: ['hard to peel boiled eggs', 'boiled egg shell sticking', 'rapid egg cooker'],
    34: ['overpacked suitcase', 'carry on suitcase explosion', 'compression packing cubes'],
    35: ['overweight baggage fee', 'airline luggage scale', 'baggage 50 lbs airport'],
    36: ['tangled appliance cords', 'extension cord knot', 'cord organizer drawer'],
    37: ['under sink clutter', 'cabinet under sink dark', 'pull out sink organizer'],
    38: ['fitted sheet popping off', 'bed sheet corner slipping', 'deep pocket sheets'],
    39: ['scrubbing grout toothbrush', 'bathroom tile grout mildew', 'power scrubber grout'],
    40: ['leggings pilling', 'fuzz on wool coat', 'fabric defuzzer pills'],
    41: ['whitehead popped scab', 'pimple patch whitehead', 'picking at acne face'],
    42: ['cracked winter lips', 'bleeding knuckles winter', 'dry hands aquaphor'],
    43: ['cracked dry fingertips', 'working hands cream', 'painful skin cracks fingers'],
    44: ['scrubbing shower glass', 'soap scum shower walls', 'daily shower cleaner spray'],
    45: ['hanging pictures apartment rental', 'command strips frames', 'drywall nail holes deposit'],
    46: ['glass french press broke', 'shattered french press sink', 'stainless steel french press'],
    47: ['apartment air dry winter', 'static shock blankets', 'room humidity monitor'],
    48: ['burned hands oven pad', 'thin potholder burn', 'silicone oven mitts skillet'],
    49: ['swollen feet long flight', 'airplane economy leg ache', 'airplane footrest hammock'],
    50: ['pet hair in laundry dryer', 'dog fur on washed clothes', 'furzapper laundry wash'],
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

    # 0. Smart API Guard: If queue already has 30+ pending viral leads, stop to conserve OpenRouter API
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM reply_approval_queue WHERE ip_id = 'emma' AND status = 'pending' AND (engagement_tier LIKE '%VIRAL%' OR likes_count >= 15)")
    pending_viral_count = c.fetchone()[0]
    conn.close()

    if pending_viral_count >= 30:
        log(f"🛑 Smart Queue Cap: Queue already has {pending_viral_count} viral pending leads. Skipping scrape & LLM evaluation.")
        return []

    if not os.path.exists(SESSION_PATH):
        log("❌ threads_session.json not found! Please login first.")
        return []

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    encoded_q = query.replace(" ", "%20")
    
    # Target TOP / VIRAL threads strictly
    search_targets = [("🔥 TOP / VIRAL", f"https://www.threads.net/search?q={encoded_q}&serp_type=default")]

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

        # 1. Strict Viral Filter: ONLY target threads with proven viral traction
        if likes < 15 and replies < 5:
            log(f"⏭️ Skipping @{author} ({likes} likes, {replies} replies) — below viral threshold (min 15 likes).")
            continue

        engagement_tier = "🔥 VIRAL HIJACK"
        opportunity_score = min(100, int(likes + (replies * 3)))

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
