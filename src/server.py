"""CareSooner server — Python standard library only, no database, no keys.

Run:  cd ~/workspace/dsh-hacks && python3 src/server.py
Then: http://localhost:8004/
Env:  PORT (default 8004). Binds 0.0.0.0 so a hosted container can serve it.
Privacy: stateless. Nothing submitted is stored on the server. The change
tracker in the browser uses the visitor's own browser storage only.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from explainer import TOPICS, RED_FLAGS, explain, visit_note  # noqa: E402

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
MAX_BODY = 64 * 1024


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep logs small; never log request bodies
        pass

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            raise ValueError("request body missing or too large")
        raw = self.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("request body must be a JSON object")
        return data

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._send_json(200, {"status": "ok", "mode": "local", "app": "CareSooner"})
        if path == "/api/topics":
            return self._send_json(200, {"topics": TOPICS, "red_flags": RED_FLAGS})
        if path in ("/", "/index.html"):
            target = os.path.join(PUBLIC_DIR, "index.html")
            with open(target, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return self._send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self._read_json()
            if path == "/api/explain":
                result = explain(
                    data.get("topic_ids", []),
                    data.get("red_flags", []),
                    data.get("duration", "not sure"),
                    data.get("pattern", "not sure"),
                )
                return self._send_json(200, result)
            if path == "/api/visit-note":
                text = visit_note(
                    data.get("topic_ids", []),
                    data.get("red_flags", []),
                    data.get("duration", "not sure"),
                    data.get("pattern", "not sure"),
                    data.get("observations", []),
                )
                return self._send_json(200, {"visit_note": text})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            return self._send_json(400, {"error": str(exc)})
        return self._send_json(404, {"error": "not found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8004"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"CareSooner running on http://localhost:{port}/ (mode: local, no storage)")
    server.serve_forever()
