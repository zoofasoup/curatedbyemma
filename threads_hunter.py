"""
Threads Target Hunter & Auto-Matcher for Hero Slots (#3, #1, #7).
Uses Playwright session to search fresh threads (<= 4h) with genuine complaints.
Records candidate threads to SQLite (data/affiliate.db).
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import db

HERO_TARGETS = {
    3: {
        "name": "Desk Lumbar Cushion",
        "keywords": [
            "office chair back pain",
            "sitting at desk back hurting",
            "lower back desk chair",
            "cheap office chair posture"
        ],
        "reply_template": "sitting all day ruined my lower back too. before you spend $600 on a whole new chair, try a high-density memory foam lumbar cushion first. literally saved my posture. kept the top-rated one at bio #3."
    },
    1: {
        "name": "Pet Hair Lint Roller",
        "keywords": [
            "dog hair couch velvet",
            "cat hair sofa vacuuming",
            "golden retriever shedding everywhere",
            "lint roller not working couch"
        ],
        "reply_template": "ugh velvet and dog hair is the absolute worst combo. standard sticky tape rollers never worked for us, but that mega extra-sticky roller has almost 40k reviews for a reason. saved the exact one under #1 in my bio if you need it."
    },
    7: {
        "name": "Airplane Tray-Table Phone Mount",
        "keywords": [
            "holding phone 4 hours flight",
            "airplane seatback neck cramp",
            "long flight holding phone",
            "tray table phone stand flight"
        ],
        "reply_template": "holding your phone for a 4-hour flight is literal neck torture. that universal tray-table clamp mount is an absolute travel essential. listed under #7 in my bio."
    }
}

SESSION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threads_session.json")

def search_hero_threads(max_per_keyword=3, headless=True):
    """
    Search Threads for hero keyword queries, filter candidates, and save to SQLite.
    """
    if not os.path.exists(SESSION_PATH):
        print("[!] threads_session.json not found! Please login first.")
        return []

    with open(SESSION_PATH, "r") as f:
        session_data = json.load(f)

    cookies = session_data.get("cookies", [])
    candidates = []

    print(f"[*] Starting Threads Hunter for 3 Hero Slots at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-ipv6'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        context.add_cookies(cookies)
        page = context.new_page()

        conn = db.get_connection()
        cur = conn.cursor()

        for slot, config in HERO_TARGETS.items():
            print(f"\n--- Scanning for Slot #{slot}: {config['name']} ---")
            for kw in config["keywords"]:
                encoded_kw = kw.replace(" ", "%20")
                search_url = f"https://www.threads.net/search?q={encoded_kw}&serp_type=default&filter=recent"
                
                try:
                    print(f"  > Searching: '{kw}'...")
                    page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
                    page.wait_for_timeout(3500)

                    # Extract thread elements
                    # Threads posts are standard article/feed items
                    posts = page.locator("div[data-pressable-container='true']").all()
                    if not posts:
                        posts = page.locator("article").all()

                    found_count = 0
                    for post in posts[:6]:
                        try:
                            text = post.inner_text().strip()
                            if not text or len(text) < 20:
                                continue

                            lines = [l.strip() for l in text.split("\n") if l.strip()]
                            author = lines[0] if lines else "unknown"
                            clean_text = " ".join(lines[1:5]) if len(lines) > 1 else text

                            # Generate a unique hash id based on text snippet
                            thread_id = f"th_{slot}_{abs(hash(clean_text[:60]))}"

                            # Check if already in DB
                            cur.execute("SELECT id FROM threads_scraped WHERE id = ?", (thread_id,))
                            if cur.fetchone():
                                continue

                            # Save to SQLite
                            cur.execute("""
                            INSERT OR IGNORE INTO threads_scraped (id, ip_id, author_username, thread_text, detected_category, matched_slot)
                            VALUES (?, 'emma', ?, ?, ?, ?)
                            """, (thread_id, author, clean_text, config["name"], slot))
                            conn.commit()

                            candidates.append({
                                "id": thread_id,
                                "slot": slot,
                                "author": author,
                                "text": clean_text,
                                "reply": config["reply_template"]
                            })
                            found_count += 1
                            if found_count >= max_per_keyword:
                                break
                        except Exception as e:
                            continue

                    print(f"    Found {found_count} fresh candidate thread(s).")
                    time.sleep(2)
                except Exception as e:
                    print(f"    [!] Error searching '{kw}': {e}")

        conn.close()
        browser.close()

    print(f"\n[✓] Hunter run finished. Total new candidates recorded in DB: {len(candidates)}")
    return candidates

if __name__ == "__main__":
    search_hero_threads(max_per_keyword=2, headless=True)
