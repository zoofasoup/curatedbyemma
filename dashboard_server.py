import os
import sys
import json
import time
import threading
from datetime import datetime
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse

from threads_engine import generate_honest_reply, match_product_slot
from threads_broadcast import CURATED_QUEUE, load_history, publish_thread, get_next_unposted

import db
import auto_worker
import catalog_manager
import threads_sniper_single

PORT = 7860
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_BUFFER = []

def get_session_health():
    session_path = os.path.join(BASE_DIR, "threads_session.json")
    if not os.path.exists(session_path):
        return {
            "healthy": False,
            "status": "missing",
            "message": "threads_session.json not found"
        }
    try:
        with open(session_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cookies = data.get("cookies", [])
        now = time.time()
        user_id = None
        min_expiry = None
        for c in cookies:
            if c.get("name") == "ds_user_id":
                user_id = c.get("value")
            exp = c.get("expires", -1)
            if exp and exp > now:
                if min_expiry is None or exp < min_expiry:
                    min_expiry = exp
        days_left = round((min_expiry - now) / 86400, 1) if min_expiry else -1
        is_healthy = len(cookies) > 5 and (days_left > 1 or days_left == -1)
        return {
            "healthy": is_healthy,
            "status": "active" if is_healthy else "expiring_soon",
            "username": "curated_byemma",
            "user_id": user_id,
            "cookies_count": len(cookies),
            "days_left": days_left
        }
    except Exception as e:
        return {
            "healthy": False,
            "status": "error",
            "message": str(e)
        }

def add_log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    LOG_BUFFER.append(entry)
    if len(LOG_BUFFER) > 100:
        LOG_BUFFER.pop(0)

class DashboardHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable cache for API
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        if path in ("/", "/control", "/control/", "/dashboard"):
            self.serve_file(os.path.join(BASE_DIR, "public", "control", "index.html"), "text/html; charset=utf-8")
        elif path == "/api/overview":
            self.handle_get_overview()
        elif path == "/api/catalog":
            self.handle_get_catalog()
        elif path == "/api/broadcast":
            self.handle_get_broadcast()
        elif path == "/api/logs":
            self.handle_get_logs()
        elif path == "/api/analytics":
            self.handle_get_analytics()
        elif path == "/api/replies":
            self.handle_get_replies()
        elif path == "/api/replies/sent":
            self.send_json({"status": "ok", "replies": db.get_approved_replies_detailed("emma")})
        elif path == "/api/queue":
            self.handle_get_queue()
        elif path == "/api/autopilot":
            self.send_json(auto_worker.get_status())
        elif path == "/api/session/health":
            self.send_json(get_session_health())
        elif path == "/api/track/stats":
            self.send_json(db.get_lander_analytics())
        elif path == "/api/track/click":
            params = urllib.parse.parse_qs(url.query)
            slot = int(params.get("slot", [0])[0]) if params.get("slot") else None
            prod = params.get("product", [""])[0]
            ref = self.headers.get("Referer", "")
            ua = self.headers.get("User-Agent", "")
            db.log_lander_event("slot_click", slot=slot, product_name=prod, referrer=ref, user_agent=ua)
            self.send_json({"status": "ok"})
        elif path.startswith("/assets/"):
            # Serve public assets (photos)
            asset_path = os.path.join(BASE_DIR, "public", path.lstrip("/"))
            if os.path.exists(asset_path):
                content_type = "image/jpeg" if asset_path.endswith((".jpg", ".jpeg")) else "image/png"
                self.serve_file(asset_path, content_type)
            else:
                self.send_error(404, "Asset not found")
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path == "/api/simulate":
            self.handle_simulate(data)
        elif path == "/api/broadcast/publish":
            self.handle_broadcast_publish(data)
        elif path == "/api/analytics/update":
            self.handle_update_metrics(data)
        elif path == "/api/automation/run":
            self.handle_run_automation(data)
        elif path == "/api/queue/approve":
            self.handle_approve_queue(data)
        elif path == "/api/queue/reject":
            self.handle_reject_queue(data)
        elif path == "/api/track":
            try:
                evt = data.get("event", "slot_click")
                slot = data.get("slot")
                slot_int = int(slot) if slot is not None else None
                prod = data.get("product", "")
                ref = data.get("referrer", self.headers.get("Referer", ""))
                ua = self.headers.get("User-Agent", "")
                db.log_lander_event(evt, slot=slot_int, product_name=prod, referrer=ref, user_agent=ua)
                self.send_json({"status": "ok"})
            except Exception as e:
                self.send_json({"error": str(e)}, status=400)
        elif path == "/api/autopilot/toggle":
            if auto_worker.WORKER_RUNNING:
                auto_worker.stop_worker()
            else:
                auto_worker.start_worker()
            self.send_json(auto_worker.get_status())
        elif path == "/api/snipe/analyze":
            target_url = data.get("url", "").strip()
            if not target_url:
                self.send_json({"error": "Missing URL"}, status=400)
                return
            res = threads_sniper_single.analyze_thread_url(target_url)
            self.send_json(res)
        elif path == "/api/snipe/dispatch":
            target_url = data.get("url", "").strip()
            reply_text = data.get("reply_text", "").strip()
            slot = int(data.get("slot", 1))
            author = data.get("author", "user")
            thread_text = data.get("thread_text", "")
            if not target_url or not reply_text:
                self.send_json({"error": "Missing parameters"}, status=400)
                return
            res = threads_sniper_single.dispatch_quick_snipe(target_url, reply_text, slot, author, thread_text)
            self.send_json(res)
        elif path == "/api/catalog/swap":
            slot = int(data.get("slot", 1))
            prod_data = data.get("product_data", {})
            if not prod_data:
                self.send_json({"error": "Missing product data"}, status=400)
                return
            success = catalog_manager.update_slot_product(slot, prod_data)
            self.send_json({"status": "ok" if success else "error", "slot": slot})
        elif path == "/api/session/update":
            raw_cookies = data.get("cookies")
            if not raw_cookies:
                self.send_json({"error": "Missing cookies"}, status=400)
                return
            try:
                if isinstance(raw_cookies, str):
                    parsed_cookies = json.loads(raw_cookies)
                else:
                    parsed_cookies = raw_cookies
                if isinstance(parsed_cookies, dict) and "cookies" in parsed_cookies:
                    parsed_cookies = parsed_cookies["cookies"]
                if not isinstance(parsed_cookies, list):
                    self.send_json({"error": "Cookies must be a list"}, status=400)
                    return
                session_path = os.path.join(BASE_DIR, "threads_session.json")
                with open(session_path, "w", encoding="utf-8") as f:
                    json.dump({"cookies": parsed_cookies}, f, indent=2)
                self.send_json({"status": "ok", "health": get_session_health()})
            except Exception as e:
                self.send_json({"error": f"Failed to save cookies: {e}"}, status=400)
        else:
            self.send_error(404, "Not Found")

    def serve_file(self, filepath, content_type):
        if not os.path.exists(filepath):
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def handle_get_overview(self):
        session_exists = os.path.exists(os.path.join(BASE_DIR, "threads_session.json"))
        history = load_history()
        successful = [h for h in history if h.get("status") == "success"]

        with open(os.path.join(BASE_DIR, "master_catalog.json"), "r") as f:
            catalog = json.load(f)

        overview = {
            "status": "online",
            "persona": {
                "name": "Emma",
                "handle": "@curated_byemma",
                "brand": "Emma's Daily Finds",
                "session_active": session_exists
            },
            "session_health": get_session_health(),
            "lander_analytics": db.get_lander_analytics(),
            "catalog_total": len(catalog),
            "landing_page_url": "https://curatedbyemma.pages.dev",
            "broadcast": {
                "total_queued": len(CURATED_QUEUE),
                "published_count": len(successful),
                "pending_count": len(CURATED_QUEUE) - len(successful)
            },
            "affiliate_tag": "curatedbyem0f-20",
            "timestamp": datetime.now().isoformat()
        }
        self.send_json(overview)

    def handle_get_catalog(self):
        with open(os.path.join(BASE_DIR, "master_catalog.json"), "r") as f:
            catalog = json.load(f)
        self.send_json(catalog)

    def handle_get_broadcast(self):
        history = load_history()
        posted_ids = {h["id"] for h in history if h.get("status") == "success"}
        
        items = []
        for q in CURATED_QUEUE:
            item_copy = dict(q)
            item_copy["published"] = q["id"] in posted_ids
            # find timestamp if published
            record = next((h for h in history if h.get("id") == q["id"] and h.get("status") == "success"), None)
            item_copy["published_at"] = record["timestamp"] if record else None
            items.append(item_copy)

        self.send_json({
            "queue": items,
            "history": history
        })

    def handle_get_logs(self):
        self.send_json({"logs": LOG_BUFFER})

    def handle_simulate(self, data):
        text = data.get("text", "")
        if not text:
            self.send_json({"error": "Missing input text"}, status=400)
            return

        add_log(f"Simulating pain point: '{text[:50]}...'")
        res = generate_honest_reply(text)
        self.send_json(res)

    def handle_broadcast_publish(self, data):
        post_id = data.get("id")
        
        if post_id:
            target = next((item for item in CURATED_QUEUE if item["id"] == post_id), None)
            if not target:
                self.send_json({"error": f"Post ID {post_id} not found"}, status=404)
                return
        else:
            target = get_next_unposted()
            if not target:
                self.send_json({"error": "All queued posts have already been published!"}, status=400)
                return

        def run_publish():
            add_log(f"Starting publish for '{target['title']}'...")
            success = publish_thread(target, headless=True)
            if success:
                add_log(f"✓ '{target['title']}' published successfully!")
            else:
                add_log(f"[X] Failed to publish '{target['title']}'.")

        # Run in separate thread so HTTP response returns immediately
        thread = threading.Thread(target=run_publish, daemon=True)
        thread.start()

        self.send_json({
            "status": "started",
            "message": f"Publish job started in background for '{target['title']}'. Check logs for updates.",
            "post_id": target["id"]
        })

    def handle_get_analytics(self):
        try:
            metrics = db.get_slot_analytics("emma")
            self.send_json({"status": "ok", "metrics": metrics})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_get_replies(self):
        try:
            replies = db.get_recent_replies("emma", limit=30)
            self.send_json({"status": "ok", "replies": replies})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_update_metrics(self, data):
        try:
            slot = int(data.get("slot"))
            ip_id = data.get("ip_id", "emma")
            clicks = data.get("amazon_clicks")
            sales = data.get("amazon_sales")
            status = data.get("status")
            notes = data.get("notes")
            db.update_slot_metrics(ip_id, slot, amazon_clicks=clicks, amazon_sales=sales, status=status, notes=notes)
            self.send_json({"status": "success", "slot": slot})
        except Exception as e:
            self.send_json({"error": str(e)}, status=400)

    def handle_run_automation(self, data):
        query = data.get("query")
        scrolls = int(data.get("scrolls", 2))
        rotate = bool(data.get("rotate", False))

        def worker():
            try:
                import threads_sniffer
                if rotate or not query:
                    add_log("🚀 Starting Multi-Slot Query Rotator across catalog...")
                    total = threads_sniffer.run_query_rotation(scrolls=scrolls, headless=True, log_callback=add_log)
                    add_log(f"✓ Sprint Rotator Completed! Found and queued {total} high-intent opportunity(s).")
                else:
                    add_log(f"🚀 Starting GraphQL Sniffer for query: '{query}'...")
                    found = threads_sniffer.run_graphql_sniffer(query=query, scrolls=scrolls, headless=True, log_callback=add_log)
                    add_log(f"✓ Sniffer Session Finished! Added {len(found)} qualified drafts to Approval Queue.")
            except Exception as e:
                add_log(f"[X] Sniffer run failed: {e}")

        t = threading.Thread(target=worker, daemon=True)
        t.start()
        self.send_json({"status": "started", "message": "GraphQL sniffer running in background"})

    def handle_get_queue(self):
        try:
            items = db.get_pending_queue("emma")
            self.send_json({"status": "ok", "queue": items})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_approve_queue(self, data):
        queue_id = int(data.get("id"))
        # Immediately set status to 'dispatching' so it is removed from pending queue in dashboard
        db.update_queue_status(queue_id, "dispatching")
        
        def worker():
            add_log(f"🚀 User approved reply #{queue_id}. Dispatching to Threads...")
            try:
                import reply_automation
                reply_automation.send_approved_reply(queue_id)
                add_log(f"✓ Reply #{queue_id} successfully sent to Threads!")
            except Exception as e:
                err_str = str(e)
                add_log(f"[X] Failed to send reply #{queue_id}: {err_str}")
                try:
                    db.update_queue_status(queue_id, "failed")
                except Exception:
                    pass
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        self.send_json({"status": "dispatching", "id": queue_id})

    def handle_reject_queue(self, data):
        try:
            queue_id = int(data.get("id"))
            db.update_queue_status(queue_id, "rejected")
            add_log(f"[-] Reply #{queue_id} discarded by user.")
            self.send_json({"status": "rejected", "id": queue_id})
        except Exception as e:
            self.send_json({"error": str(e)}, status=400)

def start_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DashboardHandler)
    add_log(f"🚀 Affiliate Engine Dashboard running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        add_log("Dashboard stopped.")
        server.server_close()

if __name__ == "__main__":
    start_server()
