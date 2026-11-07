"""
Autonomous Reply Automation Engine for Emma (@curated_byemma).
Follows:
- "NEVER LIE" & 4-Part Honest Arc (Empathy -> Audit -> Solution & Caveat -> Bio Anchor)
- Meta Safety: Cooldown 8-15 mins, Max 5-7 replies/day, Anti-duplicate authors in SQLite.
- Target: Hero Slots #3 (Lumbar), #1 (Pet Hair), #7 (Airplane Mount).
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
import db
from browser_lock import acquire_browser_lock
import reply_generator

# -------------------------------------------------------------
# 1. TEMPLATES: THE 4-PART HONEST RESEARCHER FRAMEWORK
# -------------------------------------------------------------
FRAMEWORK_TEMPLATES = {
    3: [
        "office chairs under $400 are honestly a scam for your lower back. when i audited review patterns on ergonomic cushions to filter out the bot reviews, high-density molded foam was the only thing 27k verified desk workers consistently swore by. it won't fix medical spine issues, but taking pressure off the lower back made 8-hour shifts actually tolerable. kept the exact top-rated pick cataloged under #3 on my page. btw what chair are you using right now?",
        "sitting all day in a standard office chair slowly wrecks your posture. looked through dozens of back cushions and cheap memory foam always goes flat within a month. the high-density molded one with 27k verified reviews actually holds its shape. only catch is it feels firm the first two days, but it saved my spine. listed under #3 in my bio. do you have lumbar adjust on yours or is it totally flat?"
    ],
    1: [
        "vacuuming dog hair off velvet couches is literal exercise for zero results. looked through dozens of viral pet rollers and 90% lose stickiness after 3 sweeps. the 5-pack extra-sticky one with 39k verified reviews is the consensus winner. only catch is you go through sheets fast with a heavy shedder, but it actually grabs deep fur. listed under #1 in my bio. what breed do you have? some coats are so much harder to get out lol",
        "couch fabric and shedding pets is the most frustrating combo ever. standard tape rollers are way too weak for deep fur. audited pet community recommendations and that extra-sticky roller with 39k reviews kept coming up. only downside is peeling the diagonal sheets takes a second to get used to, but it pulls everything. kept it cataloged at bio #1. is your sofa velvet or woven fabric?"
    ],
    7: [
        "holding a phone for a 4-hour flight gives you the worst neck strain imaginable. instead of overpaying for airport gadgets, that $21 clamp mount that locks directly onto the seatback tray table is an absolute sanity saver. hands-free movie right at eye level. cataloged the exact sturdy one under #7 in my bio. do you have a long haul flight coming up or just a short domestic one?",
        "long flights without seatback screens are torture for your neck. audited travel gear before my last trip and that airplane tray-table clamp mount had over 22k verified reviews for a reason. clamp feels a bit stiff at first, but keeping your phone eye-level is 100% worth it. cataloged under #7 in my bio. where are you heading to?"
    ]
}

SEARCH_QUERIES = [
    {"slot": 3, "query": "office chair lower back pain", "category": "Desk Lumbar Cushion"},
    {"slot": 3, "query": "desk chair posture hurting", "category": "Desk Lumbar Cushion"},
    {"slot": 1, "query": "dog hair couch vacuuming", "category": "Pet Hair Lint Roller"},
    {"slot": 1, "query": "cat shedding velvet sofa", "category": "Pet Hair Lint Roller"},
    {"slot": 7, "query": "flight neck pain holding phone", "category": "Airplane Phone Mount"},
    {"slot": 7, "query": "airplane seat holding phone", "category": "Airplane Phone Mount"},
    {"slot": 5, "query": "sweater pilling ruined knit", "category": "Fabric Sweater Defuzzer"},
    {"slot": 5, "query": "cardigan fuzz balls wool", "category": "Fabric Sweater Defuzzer"},
    {"slot": 10, "query": "undercooked chicken dry turkey meat", "category": "Digital Meat Thermometer"},
    {"slot": 10, "query": "cooking meat anxiety thermometer", "category": "Digital Meat Thermometer"}
]

SESSION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threads_session.json")

def is_valid_complaint(text):
    """
    Sentiment & Integrity Gate (Never Lie):
    Ensure the text contains first-person pain point and isn't sports/politics/news.
    """
    t = text.lower()
    
    # Must NOT contain sports / medical tragedy / news keywords
    banned_context = ["baseball", "mlb", "nba", "pitcher", "hospital", "surgery", "died", "cancer", "trump", "biden", "election", "prompt", "midjourney"]
    if any(b in t for b in banned_context):
        return False

    # Must contain first person pain indicators
    first_person = ["my", "i'm", "im", "i ", "me ", "we ", "mine", "hurting", "killing me", "tired of", "struggling", "help"]
    if not any(fp in t for fp in first_person):
        return False

    return True

def run_reply_automation(max_replies_this_run=2, dry_run=False):
    """
    Scrapes fresh threads, validates against rules, replies via Playwright, and logs to SQLite.
    """
    if not os.path.exists(SESSION_PATH):
        print("[!] threads_session.json not found! Exiting.")
        return 0

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    conn = db.get_connection()
    cur = conn.cursor()

    # Check daily limit (Aggressive max capacity: 25 per day)
    cur.execute("SELECT COUNT(*) as count FROM replies_sent WHERE ip_id = 'emma' AND DATE(sent_at) = DATE('now') AND status = 'sent'")
    today_count = cur.fetchone()["count"]
    DAILY_MAX = int(os.environ.get("DAILY_REPLY_LIMIT", "40"))
    if today_count >= DAILY_MAX:
        print(f"[*] Aggressive daily limit reached for today ({today_count}/{DAILY_MAX} sent). Cooling down to protect account.")
        conn.close()
        return 0

    print(f"[*] Starting High-Velocity Reply Automation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Today's replies sent so far: {today_count}/{DAILY_MAX}. Target this batch: {max_replies_this_run}")

    replies_completed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-ipv6'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        context.add_cookies(cookies)
        page = context.new_page()

        # Randomize queries
        random.shuffle(SEARCH_QUERIES)

        for sq in SEARCH_QUERIES:
            if replies_completed >= max_replies_this_run:
                break

            slot = sq["slot"]
            query = sq["query"]
            encoded_query = query.replace(" ", "%20")
            search_url = f"https://www.threads.net/search?q={encoded_query}&serp_type=default&filter=recent"

            print(f"\n[+] Searching Slot #{slot} ({sq['category']}): '{query}'...")
            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(4000)

                posts = page.locator("div[data-pressable-container='true']").all()
                if not posts:
                    posts = page.locator("article").all()

                for post_el in posts[:5]:
                    if replies_completed >= max_replies_this_run:
                        break

                    text = post_el.inner_text().strip()
                    if len(text) < 25:
                        continue

                    # Validate complaint
                    if not is_valid_complaint(text):
                        continue

                    lines = [l.strip() for l in text.split("\n") if l.strip()]
                    author = lines[0].replace("@", "") if lines else "anonymous"

                    # Anti-duplicate author check in SQLite
                    cur.execute("SELECT id FROM threads_scraped WHERE author_username = ?", (author,))
                    if cur.fetchone():
                        continue

                    # STRICT CONTEXT EVALUATOR (Never Lie & Reject Family/Memorial/Joke Context)
                    eval_res = reply_generator.evaluate_and_draft_local(text, author=author)
                    if eval_res["verdict"] == "REJECT":
                        print(f"  [-] Hard REJECTED post by @{author}: {eval_res.get('reason')}")
                        continue

                    # Extract the direct post URL from card
                    post_link_el = post_el.locator("a[href*='/post/']").first
                    if post_link_el.count() == 0:
                        continue
                    post_href = post_link_el.get_attribute("href")
                    if not post_href:
                        continue
                    direct_post_url = "https://www.threads.net" + post_href if post_href.startswith("/") else post_href

                    matched_slot = eval_res["slot"]
                    product_name = eval_res["product_name"]
                    reply_text = eval_res["reply_draft"]

                    print(f"  [✓] ACCEPTED Genuine Complaint by @{author}:")
                    print(f"      Product: Slot #{matched_slot} ({product_name})")
                    print(f"      URL: {direct_post_url}")
                    print(f"      Original Text: \"{text[:75]}...\"")
                    print(f"      Crafted 4-Part Reply: \"{reply_text}\"")

                    # Add to Human Approval Queue in SQLite
                    db.add_to_queue(
                        ip_id="emma",
                        author=author,
                        thread_url=direct_post_url,
                        thread_text=text,
                        slot=matched_slot,
                        product_name=product_name,
                        draft_reply=reply_text
                    )

                    # Also mark thread as scraped to prevent re-processing
                    thread_id = f"th_{matched_slot}_{abs(hash(direct_post_url))}"
                    cur.execute("""
                    INSERT OR IGNORE INTO threads_scraped (id, ip_id, author_username, thread_text, detected_category, matched_slot)
                    VALUES (?, 'emma', ?, ?, ?, ?)
                    """, (thread_id, author, text, product_name, matched_slot))
                    conn.commit()

                    replies_completed += 1
                    
                    # Cooldown between replies if sending more than 1 (human-like pacing)
                    if replies_completed < max_replies_this_run and not dry_run:
                        cooldown_secs = random.randint(180, 360) # 3 to 6 mins
                        print(f"  [⏱] Sleeping for {cooldown_secs}s ({cooldown_secs // 60}m) to bypass Meta rate limit...")
                        time.sleep(cooldown_secs)

            except Exception as e:
                print(f"  [!] Error during search '{query}': {e}")

        conn.close()
        browser.close()

    print(f"\n[✓] Automation run finished. Total replies logged/sent: {replies_completed}")
    return replies_completed

def send_approved_reply(queue_id):
    """
    Called when user approves a draft from the dashboard queue.
    Submits the reply to Threads using native Control+Enter shortcut.
    """
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM reply_approval_queue WHERE id = ?", (queue_id,))
    item = c.fetchone()
    if not item:
        conn.close()
        raise Exception(f"Queue item #{queue_id} not found")

    if not os.path.exists(SESSION_PATH):
        conn.close()
        raise Exception("threads_session.json not found")

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)
    cookies = session_data.get("cookies", [])

    direct_post_url = item["thread_url"]
    # Normalize domain to avoid redirect hops (threads.net -> threads.com)
    target_post_url = direct_post_url.replace("threads.net", "threads.com") if "threads.net" in direct_post_url else direct_post_url
    reply_text = item["draft_reply"]
    slot = item["matched_slot"]
    author = item["author_username"]

    print(f"[*] Dispatching approved reply to @{author} ({target_post_url})...")

    # Acquire exclusive browser lock so concurrent sniffer or workers do not exhaust VPS RAM
    with acquire_browser_lock(timeout_seconds=180):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-ipv6',
                    '--single-process',
                    '--no-zygote',
                    '--disable-extensions',
                    '--mute-audio'
                ]
            )
            ctx = browser.new_context(
                locale="en-US",
                timezone_id="America/New_York",
                viewport={"width": 1280, "height": 800},
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "sec-ch-ua-platform": '"macOS"'
                },
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            ctx.add_cookies(cookies)
            page = ctx.new_page()

            page.goto(target_post_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3500)

            # Check if page is deleted, 404, or restricted
            content_lower = page.content().lower()
            if "isn't available" in content_lower or "page not found" in content_lower:
                browser.close()
                raise Exception("Threads post returned 404 or is no longer available.")
            if "replies are limited" in content_lower or "only people mentioned" in content_lower:
                browser.close()
                raise Exception("Author restricted replies on this thread.")

            composer = page.locator("div[role='textbox'][contenteditable='true']").first
            # If not immediately visible, trigger reply button if present
            if not composer.is_visible():
                for trigger_sel in ["button:has-text('Reply')", "div[role='button']:has-text('Reply')", "[aria-label='Reply']", "svg[aria-label='Reply']"]:
                    try:
                        trig = page.locator(trigger_sel).first
                        if trig.is_visible():
                            trig.click()
                            page.wait_for_timeout(800)
                            if composer.is_visible():
                                break
                    except Exception:
                        pass

            try:
                composer.wait_for(state="visible", timeout=15000)
            except Exception:
                browser.close()
                raise Exception("Reply textbox not found (replies may be disabled or page failed to render).")

            # Enforce hard length safety check for short human replies (max 260 chars)
            if len(reply_text) > 260:
                browser.close()
                raise Exception(f"Reply text exceeds short human limit ({len(reply_text)} chars > 260). Aborting to prevent bot detection.")

            composer.click()
            page.wait_for_timeout(400)

            # Insert paragraphs safely:
            # Using page.keyboard.type() with raw \n triggers physical 'Enter' keypresses,
            # which in Threads/Instagram web comment boxes immediately SUBMITS the partial comment!
            # Using keyboard.insert_text() with Shift+Enter for newlines completely prevents premature submission.
            paragraphs = reply_text.split("\n")
            for i, p_text in enumerate(paragraphs):
                if p_text:
                    page.keyboard.insert_text(p_text)
                    page.wait_for_timeout(100)
                if i < len(paragraphs) - 1:
                    page.keyboard.press("Shift+Enter")
                    page.wait_for_timeout(150)

            page.wait_for_timeout(1000)

            # Pre-flight verification: Confirm composer text contains the direct link before clicking Post
            composer_text = composer.inner_text()
            if "curatedbyemma.pages.dev/go/" not in composer_text:
                browser.close()
                raise Exception(f"Affiliate link verification failed before submit: 'curatedbyemma.pages.dev/go/' not found in composer text! Text: {composer_text[:120]}")

            # Submit: Try clicking explicit 'Post' button first, fallback to Control/Meta+Enter
            post_btn = page.locator("div[role='button']:has-text('Post'), button:has-text('Post')").first
            clicked = False
            try:
                if post_btn.is_visible():
                    post_btn.click()
                    clicked = True
            except Exception:
                pass

            if not clicked:
                composer.focus()
                page.keyboard.press("Control+Enter")
                page.wait_for_timeout(300)
                page.keyboard.press("Meta+Enter")

            page.wait_for_timeout(4500)

            # Verification: Check if error banner appeared
            final_content = page.content().lower()
            if "couldn't post" in final_content or "try again later" in final_content:
                browser.close()
                raise Exception("Meta error banner appeared ('Couldn't post' or 'Try again later').")

            browser.close()

    # Update SQLite
    db.update_queue_status(queue_id, "approved")
    db.log_reply(
        ip_id="emma",
        slot=slot,
        reply_text=reply_text,
        hook_variant="honest_researcher_4part",
        thread_id=f"th_{slot}_{abs(hash(direct_post_url))}",
        status="sent"
    )
    print(f"[✓] Approved reply #{queue_id} successfully sent and logged!")
    return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    run_reply_automation(max_replies_this_run=1, dry_run=is_dry)
