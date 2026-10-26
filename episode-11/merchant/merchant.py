# A pretend paid API, port 4061. It asks for payment with HTTP
# 402, like the x402 idea. PRETEND money only: no wallet, no
# blockchain, nothing real is ever paid.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PRICE = {"amount": 2, "currency": "pretend-cents",
         "recipient": "weather-co"}


class Merchant(BaseHTTPRequestHandler):
    def do_GET(self):
        proof = self.headers.get("X-PAYMENT")
        if not (proof and proof.startswith("pretend-proof")):
            body, status = PRICE, 402  # 402 = Payment Required
        else:
            body, status = {"report": "Chennai: 31 C, sunny"}, 200
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


print("Pretend paid API on http://localhost:4061")
HTTPServer(("localhost", 4061), Merchant).serve_forever()
