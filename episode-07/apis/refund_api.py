# A normal REST API for orders and refunds, port 4021. No AI here.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ORDERS = {"ORD-1": {"total": 800}, "ORD-2": {"total": 2400}}


class RefundApi(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")
        if parts[0] == "orders" and len(parts) == 2:
            body = ORDERS.get(parts[1], {"error": "no such order"})
        elif parts[0] == "refunds" and len(parts) == 3:
            # /refunds/ORD-1/500 -> refund 500 on order ORD-1
            body = {"refunded": int(parts[2]), "order": parts[1]}
        elif parts[0] == "delete" and len(parts) == 2:
            body = {"deleted": parts[1]}
        else:
            body = {"error": "not found"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


HTTPServer(("localhost", 4021), RefundApi).serve_forever()
