"""Local read-only teaching application. Bind to loopback; creates no AWS resources."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
from order_tool import get_order

ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path)
        if path.path == "/api/order":
            order_id = parse_qs(path.query).get("id", [""])[0]
            result = get_order(order_id)
            body = json.dumps(result, indent=2).encode()
            self.send_response(404 if "error" in result else 200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            print(json.dumps({"tool": "get_order", "arguments": {"order_id": order_id}, "result": result}), flush=True)
            return
        pages = {"/": "demo.html", "/diagrams": "diagrams.html", "/source": "order_tool.py"}
        name = pages.get(path.path)
        if not name or not (ROOT / name).is_file():
            self.send_error(404)
            return
        data = (ROOT / name).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8" if name.endswith(".py") else "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print("Local tool demo: http://127.0.0.1:8768/ — no AWS calls", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8768), Handler).serve_forever()
