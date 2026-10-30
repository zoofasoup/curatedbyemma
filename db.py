"""
Database module for Affiliate Engine testing & conversion tracking.
SQLite database located at data/affiliate.db.
"""

import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "affiliate.db")

def get_connection(timeout=30.0):
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=timeout)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # 1. Scraped target threads
    c.execute("""
    CREATE TABLE IF NOT EXISTS threads_scraped (
        id TEXT PRIMARY KEY,
        ip_id TEXT NOT NULL,
        author_username TEXT,
        thread_text TEXT NOT NULL,
        thread_url TEXT,
        detected_category TEXT,
        matched_slot INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Sent / Queued Replies
    c.execute("""
    CREATE TABLE IF NOT EXISTS replies_sent (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_id TEXT NOT NULL,
        thread_id TEXT,
        slot INTEGER NOT NULL,
        hook_variant TEXT,
        reply_text TEXT NOT NULL,
        status TEXT DEFAULT 'sent', -- 'sent', 'queued', 'failed'
        threads_post_id TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (thread_id) REFERENCES threads_scraped (id)
    )
    """)

    # 2B. Review Queue for Human-In-The-Loop Approval
    c.execute("""
    CREATE TABLE IF NOT EXISTS reply_approval_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_id TEXT NOT NULL,
        author_username TEXT,
        thread_url TEXT NOT NULL,
        thread_text TEXT NOT NULL,
        matched_slot INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        draft_reply TEXT NOT NULL,
        status TEXT DEFAULT 'pending', -- 'pending', 'dispatching', 'approved', 'rejected', 'failed'
        engagement_tier TEXT DEFAULT 'FRESH_SNIPER',
        likes_count INTEGER DEFAULT 0,
        replies_count INTEGER DEFAULT 0,
        opportunity_score INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Ensure unique index on (ip_id, thread_url) to guarantee strict deduplication
    c.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_queue_ip_url ON reply_approval_queue (ip_id, thread_url);
    """)

    # Migrate columns if existing DB created without them
    c.execute("PRAGMA table_info(reply_approval_queue)")
    cols = [col[1] for col in c.fetchall()]
    if "engagement_tier" not in cols:
        c.execute("ALTER TABLE reply_approval_queue ADD COLUMN engagement_tier TEXT DEFAULT 'FRESH_SNIPER'")
    if "likes_count" not in cols:
        c.execute("ALTER TABLE reply_approval_queue ADD COLUMN likes_count INTEGER DEFAULT 0")
    if "replies_count" not in cols:
        c.execute("ALTER TABLE reply_approval_queue ADD COLUMN replies_count INTEGER DEFAULT 0")
    if "opportunity_score" not in cols:
        c.execute("ALTER TABLE reply_approval_queue ADD COLUMN opportunity_score INTEGER DEFAULT 0")

    # 3. Slot Experiment & 7-Day Performance Metrics
    c.execute("""
    CREATE TABLE IF NOT EXISTS slot_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_id TEXT NOT NULL,
        slot INTEGER NOT NULL,
        period_start DATE NOT NULL,
        period_end DATE NOT NULL,
        replies_target INTEGER DEFAULT 20,
        replies_sent INTEGER DEFAULT 0,
        profile_clicks INTEGER DEFAULT 0,
        lander_clicks INTEGER DEFAULT 0,
        amazon_clicks INTEGER DEFAULT 0,
        amazon_sales INTEGER DEFAULT 0,
        commission_usd REAL DEFAULT 0.0,
        status TEXT DEFAULT 'testing', -- 'winner', 'testing', 'underperforming'
        notes TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ip_id, slot, period_start)
    )
    """)

    # Pre-populate Emma's slots 1-10 for current 7-day cycle if empty
    today = datetime.utcnow().strftime("%Y-%m-%d")
    for slot in range(1, 11):
        c.execute("""
        INSERT OR IGNORE INTO slot_metrics (ip_id, slot, period_start, period_end, replies_target, replies_sent, status)
        VALUES ('emma', ?, '2026-10-28', '2026-11-04', 20, 0, 'testing')
        """, (slot,))

    conn.commit()
    conn.close()

def get_slot_analytics(ip_id="emma"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT 
        sm.*,
        (SELECT COUNT(*) FROM replies_sent r WHERE r.ip_id = sm.ip_id AND r.slot = sm.slot AND r.status = 'sent') as live_replies_count
    FROM slot_metrics sm
    WHERE sm.ip_id = ?
    ORDER BY sm.slot ASC
    """, (ip_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_pending_queue(ip_id="emma"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT * FROM reply_approval_queue 
    WHERE ip_id = ? AND status = 'pending'
    ORDER BY opportunity_score DESC, created_at DESC
    """, (ip_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_pending_queue_count(ip_id="emma") -> int:
    conn = get_connection()
    c = conn.cursor()
    count = c.execute("SELECT count(*) FROM reply_approval_queue WHERE ip_id = ? AND status = 'pending'", (ip_id,)).fetchone()[0]
    conn.close()
    return count

def is_thread_already_processed(thread_url: str, ip_id: str = "emma") -> bool:
    """
    Strict deduplication check across:
    1. reply_approval_queue (pending, dispatching, approved, rejected, failed)
    2. threads_scraped (if previously ingested)
    3. replies_sent (threads already replied to)
    """
    if not thread_url:
        return False
    norm_url = thread_url.strip().split("?")[0].rstrip("/")
    conn = get_connection()
    c = conn.cursor()
    
    # Check queue
    c.execute("""
    SELECT id FROM reply_approval_queue 
    WHERE ip_id = ? AND (thread_url = ? OR thread_url LIKE ?)
    """, (ip_id, thread_url, norm_url + "%"))
    if c.fetchone():
        conn.close()
        return True

    # Check threads_scraped
    c.execute("""
    SELECT id FROM threads_scraped 
    WHERE ip_id = ? AND (thread_url = ? OR thread_url LIKE ?)
    """, (ip_id, thread_url, norm_url + "%"))
    if c.fetchone():
        conn.close()
        return True

    conn.close()
    return False

def add_to_queue(ip_id, author, thread_url, thread_text, slot, product_name, draft_reply, 
                 engagement_tier="FRESH_SNIPER", likes_count=0, replies_count=0, opportunity_score=0):
    if is_thread_already_processed(thread_url, ip_id=ip_id):
        return False
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
        INSERT INTO reply_approval_queue 
        (ip_id, author_username, thread_url, thread_text, matched_slot, product_name, draft_reply, 
         status, engagement_tier, likes_count, replies_count, opportunity_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)
        """, (ip_id, author, thread_url, thread_text, slot, product_name, draft_reply,
              engagement_tier, likes_count, replies_count, opportunity_score))
        conn.commit()
        added = True
    except sqlite3.IntegrityError:
        added = False
    finally:
        conn.close()
    return added

def update_queue_status(queue_id, new_status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE reply_approval_queue SET status = ? WHERE id = ?", (new_status, queue_id))
    conn.commit()
    conn.close()

def get_recent_replies(ip_id="emma", limit=20):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT r.*, t.author_username, t.thread_text, t.thread_url
    FROM replies_sent r
    LEFT JOIN threads_scraped t ON r.thread_id = t.id
    WHERE r.ip_id = ?
    ORDER BY r.sent_at DESC
    LIMIT ?
    """, (ip_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def log_reply(ip_id, slot, reply_text, hook_variant="empathy_first", thread_id=None, status="sent"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO replies_sent (ip_id, thread_id, slot, hook_variant, reply_text, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (ip_id, thread_id, slot, hook_variant, reply_text, status))
    
    # Update replies_sent counter in current active cycle
    c.execute("""
    UPDATE slot_metrics 
    SET replies_sent = replies_sent + 1, updated_at = CURRENT_TIMESTAMP
    WHERE ip_id = ? AND slot = ? AND status != 'archived'
    """, (ip_id, slot))
    
    conn.commit()
    conn.close()

def update_slot_metrics(ip_id, slot, amazon_clicks=None, amazon_sales=None, status=None, notes=None):
    conn = get_connection()
    c = conn.cursor()
    updates = []
    params = []
    if amazon_clicks is not None:
        updates.append("amazon_clicks = ?")
        params.append(amazon_clicks)
    if amazon_sales is not None:
        updates.append("amazon_sales = ?")
        params.append(amazon_sales)
    if status is not None:
        updates.append("status = ?")
        params.append(status)
    if notes is not None:
        updates.append("notes = ?")
        params.append(notes)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE slot_metrics SET {', '.join(updates)} WHERE ip_id = ? AND slot = ?"
        params.extend([ip_id, slot])
        c.execute(query, tuple(params))
        conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
