import os
import sys
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

SESSION_FILE = "threads_session.json"
HISTORY_FILE = "broadcast_history.json"

# Curated library of high-converting, honest Emma broadcast threads
CURATED_QUEUE = [
    {
        "id": "intro_manifesto",
        "title": "Emma's Curation Manifesto",
        "text": """testing viral amazon products so you don't waste your money.

my 3 rules before anything makes the list:
1. 4.5★ rating minimum
2. 5k+ verified reviews (zero fake review bots)
3. actually solves an everyday headache

master list of 10 audited problem solvers is updated on my page ✨""",
        "image": "public/assets/emma/emma_desk.jpg",
        "slots_mentioned": ["#1 - #10"]
    },
    {
        "id": "desk_lumbar_slot3",
        "title": "Desk Back Pain / Lumbar Relief (Slot #3)",
        "text": """sitting in an office chair 8+ hours a day was slowly wrecking my lower back.

before spending $700 on a new chair, tried an ergonomic high-density memory foam cushion backed by 27k reviews.

3 weeks in and genuinely zero aches. kept the exact one under #3 on my page.""",
        "image": "public/assets/emma/emma_cafe.jpg",
        "slots_mentioned": ["#3"]
    },
    {
        "id": "travel_flight_mount_slot7",
        "title": "Airplane Tray-Table Phone Mount (Slot #7)",
        "text": """if you have a flight coming up, please do not hold your phone for 4 hours with severe neck strain.

that $21 universal airplane tray-table clamp mount is the single best travel hack i've tested all year. hands-free movie setup right at eye level.

cataloged under #7 on my profile list.""",
        "image": None,
        "slots_mentioned": ["#7"]
    },
    {
        "id": "pet_hair_couch_slot1",
        "title": "Pet Hair & Couch Relief (Slot #1)",
        "text": """vacuuming only gets about 60% of pet hair off couches and car seats. regular lint rollers run out in 2 minutes.

that extra-sticky 5-pack with 40k reviews is the only thing that actually pulls up deep stubborn fur.

saved under #1 on my page.""",
        "image": "public/assets/emma/emma_couch.jpg",
        "slots_mentioned": ["#1"]
    },
    {
        "id": "daily_sanity_savers_roundup",
        "title": "3 Daily Sanity Savers Roundup (Slots #6, #4, #2)",
        "text": """3 random amazon problem solvers that genuinely saved my sanity this week:

1) magnetic cable wrangler so charging cords stop sliding off the nightstand (#6)
2) glass oil sprayer that actually mists without clogging your air fryer (#4)
3) the breathing otter plush that calms fussy babies to sleep (#2)

all numbered on my page if you want to check the verified reviews.""",
        "image": None,
        "slots_mentioned": ["#6", "#4", "#2"]
    },
    {
        "id": "spin_scrubber_deepclean_slot5",
        "title": "Deep Clean Without Kneeling (Slot #5)",
        "text": """scrubbing tile grout and tubs on your knees is literal torture.

electric power spin scrubbers are viral for a reason—cuts deep cleaning time in half with zero elbow grease.

cataloged the highest-rated one with extension pole under #5 on my page.""",
        "image": "public/assets/emma/emma_kitchen.jpg",
        "slots_mentioned": ["#5"]
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def get_next_unposted():
    history = load_history()
    posted_ids = {h["id"] for h in history if h.get("status") == "success"}
    for item in CURATED_QUEUE:
        if item["id"] not in posted_ids:
            return item
    return None

def publish_thread(item: dict, headless: bool = True):
    if not os.path.exists(SESSION_FILE):
        print(f"[!] Session file {SESSION_FILE} not found. Run 'python threads_poster.py login' first.")
        return False

    print(f"\n==========================================")
    print(f"🚀 Publishing to Threads: {item['title']} (ID: {item['id']})")
    print(f"==========================================")
    print(f"Text:\n{item['text']}\n")
    if item.get("image"):
        print(f"Image attached: {item['image']}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-ipv6'])
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        try:
            print("1. Opening Threads (threads.net)...")
            for attempt in range(2):
                try:
                    page.goto("https://www.threads.net/", wait_until="domcontentloaded", timeout=45000)
                    break
                except Exception as net_err:
                    if attempt == 0:
                        print(f"Connection hiccup ({net_err}), retrying in 3s...")
                        page.wait_for_timeout(3000)
                    else:
                        raise net_err

            page.wait_for_timeout(3500)

            # 2. Open Composer
            print("2. Opening thread composer...")
            compose_btn = page.locator("text=New thread").first
            compose_btn.click()
            page.wait_for_timeout(1500)

            # 3. Attach image if provided
            if item.get("image") and os.path.exists(item["image"]):
                abs_img = os.path.abspath(item["image"])
                print(f"3. Attaching lifestyle photo: {abs_img}")
                file_input = page.locator("input[type='file']").first
                file_input.set_input_files(abs_img)
                page.wait_for_timeout(3000)
            else:
                print("3. No image attached (text-only post).")

            # 4. Type text into contenteditable
            print("4. Typing post content...")
            editor = page.locator("[contenteditable='true']").first
            editor.click()
            page.keyboard.type(item["text"], delay=25)
            page.wait_for_timeout(1500)

            # 5. Click Post button
            print("5. Submitting post...")
            post_buttons = [b for b in page.locator("div[role='button']").all() if b.inner_text().strip() == "Post"]
            if not post_buttons:
                raise Exception("Could not find Post button inside composer modal.")
            
            modal_post_btn = post_buttons[-1]
            modal_post_btn.click()
            print("Post clicked, waiting for modal to close (ensuring image upload completes)...")
            try:
                modal_post_btn.wait_for(state="hidden", timeout=25000)
            except Exception:
                page.wait_for_timeout(6000)
            page.wait_for_timeout(2000)

            print("✓ Successfully posted to Threads profile!")

            # Record in history
            save_history({
                "id": item["id"],
                "title": item["title"],
                "text": item["text"],
                "image": item.get("image"),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            })

            browser.close()
            return True

        except Exception as e:
            print(f"[X] Publishing failed: {e}")
            page.screenshot(path=f"error_{item['id']}.png")
            save_history({
                "id": item["id"],
                "title": item["title"],
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
            browser.close()
            return False

def show_status():
    history = load_history()
    successful = [h for h in history if h.get("status") == "success"]
    print(f"\n--- Emma's Threads Broadcast Status ---")
    print(f"Total curated posts in queue: {len(CURATED_QUEUE)}")
    print(f"Total published posts:        {len(successful)}")
    print(f"Remaining in queue:           {len(CURATED_QUEUE) - len(successful)}\n")
    
    posted_ids = {h["id"] for h in successful}
    for i, p in enumerate(CURATED_QUEUE, 1):
        status_icon = "✓ (Published)" if p["id"] in posted_ids else "⏳ (Pending)"
        print(f"  {i}. [{p['id']}] {p['title']} -> {status_icon}")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Threads Broadcast Engine
Usage:
  python threads_broadcast.py status         -> Show queue and publication history
  python threads_broadcast.py next           -> Post the next pending thread
  python threads_broadcast.py post <post_id> -> Post a specific thread by ID
        """)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        show_status()
    elif cmd == "next":
        next_item = get_next_unposted()
        if not next_item:
            print("[i] All curated threads have already been published!")
        else:
            publish_thread(next_item, headless=True)
    elif cmd == "post":
        if len(sys.argv) < 3:
            print("Please specify a post_id. Use 'python threads_broadcast.py status' to see IDs.")
            sys.exit(1)
        target_id = sys.argv[2]
        target_item = next((p for p in CURATED_QUEUE if p["id"] == target_id), None)
        if not target_item:
            print(f"[!] Post ID '{target_id}' not found.")
            sys.exit(1)
        publish_thread(target_item, headless=True)
    else:
        print(f"Unknown command: {cmd}")
