# The agent side: call the paid API, and when it answers 402,
# pay from the session and retry with the proof. Port 3019.
import json
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from wallet import PaymentSession

HERE = Path(__file__).parent
API = "http://localhost:4061/report"
session = PaymentSession(max_spend=5, minutes=10)


def get(headers):
    try:
        with urlopen(Request(API, headers=headers)) as r:
            return r.status, json.loads(r.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def buy(send):
    status, body = get({})
    send("ask", f"Called the API: {status}", body)
    if status != 402:
        return
    try:
        proof = session.pay(body)
    except PermissionError as error:
        return send("deny", "Payment refused", str(error))
    send("pay", f"Paid {body['amount']} pretend cents",
         {"X-PAYMENT": proof, "spent": session.spent,
          "limit": session.max_spend})
    status, body = get({"X-PAYMENT": proof})
    send("done", f"Retried with proof: {status}", body)


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/buy":
            page = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        cards = []
        buy(lambda who, title, data: cards.append(
            {"who": who, "title": title, "data": data}))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(cards).encode())


print("Agent page on http://localhost:3019")
ThreadingHTTPServer(("localhost", 3019), Page).serve_forever()
