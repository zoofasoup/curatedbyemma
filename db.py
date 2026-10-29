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
