"""
Auto-Approve Dispatcher & Safe Daily Quota Engine.
Automates dispatching high-opportunity Threads replies at human-paced intervals,
strictly capped at a safe daily threshold (default: 25 replies/day).
"""

import os
import sys
import time
import random
import threading
from datetime import datetime
import db
import reply_automation

DAILY_LIMIT = 25
MIN_DELAY_SECONDS = 420  # 7 minutes
MAX_DELAY_SECONDS = 900  # 15 minutes

WORKER_RUNNING = False
WORKER_THREAD = None
LAST_DISPATCH_TIME = None
NEXT_DISPATCH_TIME = None
WORKER_LOGS = []

def get_next_target_preview():
    """Returns metadata of the next pending lead AutoPilot will target."""
    try:
        conn = db.get_connection()
        c = conn.cursor()
        c.execute("""
        SELECT id, author_username, matched_slot, product_name, engagement_tier, opportunity_score 
        FROM reply_approval_queue 
        WHERE ip_id = 'emma' AND status = 'pending'
        ORDER BY opportunity_score DESC, likes_count DESC, created_at DESC
        LIMIT 1
        """)
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "id": row["id"],
                "author": row["author_username"],
                "slot": row["matched_slot"],
                "product": row["product_name"],
                "tier": row["engagement_tier"],
                "score": row["opportunity_score"]
            }
    except Exception:
        pass
    return None

def worker_log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [AutoPilot] {msg}"
    print(entry)
    sys.stdout.flush()
    WORKER_LOGS.append(entry)
    if len(WORKER_LOGS) > 100:
        WORKER_LOGS.pop(0)

def get_sent_today_count(ip_id="emma") -> int:
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT COUNT(*) FROM replies_sent 
    WHERE ip_id = ? AND date(sent_at) = date('now')
    """, (ip_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def dispatch_next_highest_opportunity():
    """
    Selects the single highest ROI lead currently in pending queue
    (prioritizing Viral Hijack, then fresh snipers) and dispatches it.
    """
    global LAST_DISPATCH_TIME
    sent_today = get_sent_today_count()
    if sent_today >= DAILY_LIMIT:
        worker_log(f"🛑 Daily quota reached ({sent_today}/{DAILY_LIMIT} sent today). Pausing until tomorrow.")
        return False, "quota_reached"

    conn = db.get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT id, author_username, matched_slot, product_name, engagement_tier, likes_count, replies_count, opportunity_score 
    FROM reply_approval_queue 
    WHERE ip_id = 'emma' AND status = 'pending'
    ORDER BY opportunity_score DESC, likes_count DESC, created_at DESC
    LIMIT 1
    """)
    item = c.fetchone()
    conn.close()

    if not item:
        worker_log("💤 No pending items in queue. Waiting for next crawler run.")
        return False, "queue_empty"

    queue_id = item["id"]
    author = item["author_username"]
    slot = item["matched_slot"]
    tier = item["engagement_tier"]
    score = item["opportunity_score"]

    worker_log(f"🚀 Auto-approving lead #{queue_id} (@{author} | {tier} | Score: {score} | Slot #{slot})...")
    
    # Set to dispatching immediately
    db.update_queue_status(queue_id, "dispatching")

    try:
        reply_automation.send_approved_reply(queue_id)
        LAST_DISPATCH_TIME = time.time()
        sent_now = get_sent_today_count()
        worker_log(f"✅ Dispatched successfully to @{author}! Today's progress: {sent_now}/{DAILY_LIMIT}")
        return True, "success"
    except Exception as e:
        worker_log(f"❌ Failed to dispatch #{queue_id}: {e}")
        db.update_queue_status(queue_id, "failed")
        return False, f"error: {e}"

def worker_loop():
    global WORKER_RUNNING, NEXT_DISPATCH_TIME
    worker_log(f"🟢 AutoPilot Worker started! Daily limit: {DAILY_LIMIT} replies/day.")
    while WORKER_RUNNING:
        sent_today = get_sent_today_count()
        if sent_today >= DAILY_LIMIT:
            worker_log(f"Daily quota reached ({sent_today}/{DAILY_LIMIT}). Sleeping for 30 minutes...")
            NEXT_DISPATCH_TIME = time.time() + 1800
            time.sleep(1800)
            NEXT_DISPATCH_TIME = None
            continue

        dispatched, status = dispatch_next_highest_opportunity()

        if dispatched:
            # Human-like random delay before next dispatch
            delay = random.randint(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
            minutes = round(delay / 60, 1)
            worker_log(f"⏳ Sleeping {minutes} mins ({delay}s) before next check to stay natural & safe...")
            NEXT_DISPATCH_TIME = time.time() + delay
            for _ in range(delay):
                if not WORKER_RUNNING:
                    break
                time.sleep(1)
            NEXT_DISPATCH_TIME = None
        elif status == "queue_empty":
            # Queue empty, check again in 3 minutes
            NEXT_DISPATCH_TIME = time.time() + 180
            time.sleep(180)
            NEXT_DISPATCH_TIME = None
        else:
            time.sleep(60)

    NEXT_DISPATCH_TIME = None
    worker_log("🔴 AutoPilot Worker stopped.")

def start_worker():
    global WORKER_RUNNING, WORKER_THREAD
    if WORKER_RUNNING:
        return True
    WORKER_RUNNING = True
    WORKER_THREAD = threading.Thread(target=worker_loop, daemon=True)
    WORKER_THREAD.start()
    return True

def stop_worker():
    global WORKER_RUNNING, NEXT_DISPATCH_TIME
    WORKER_RUNNING = False
    NEXT_DISPATCH_TIME = None
    return True

def get_status():
    sent_today = get_sent_today_count()
    return {
        "running": WORKER_RUNNING,
        "sent_today": sent_today,
        "daily_limit": DAILY_LIMIT,
        "last_dispatch": LAST_DISPATCH_TIME,
        "next_dispatch_time": NEXT_DISPATCH_TIME,
        "next_target": get_next_target_preview() if WORKER_RUNNING else None,
        "recent_logs": WORKER_LOGS[-10:]
    }

if __name__ == "__main__":
    start_worker()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_worker()
