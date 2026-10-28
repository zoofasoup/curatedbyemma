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

PORT = 7860
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_BUFFER = []

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

        if path == "/" or path == "/dashboard":
            self.serve_file(os.path.join(BASE_DIR, "dashboard.html"), "text/html")
        elif path == "/api/overview":
            self.handle_get_overview()
        elif path == "/api/catalog":
            self.handle_get_catalog()
        elif path == "/api/broadcast":
            self.handle_get_broadcast()
        elif path == "/api/logs":
            self.handle_get_logs()
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
