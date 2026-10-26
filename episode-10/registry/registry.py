# A tiny agent registry, port 4051, like AWS Agent Registry:
# a catalog of records (agents, MCP servers, skills) with an
# approval step. Search only ever returns APPROVED records.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).parent
RECORDS = json.loads((HERE / "seed.json").read_text())


def find(name):
    return next(r for r in RECORDS if r["name"] == name)


def approve(q):  # the curator says yes
    find(q["name"])["status"] = "APPROVED"
    return {"approved": q["name"]}


def search(q):  # what agents see: approved records only
    words = [w[:4] for w in q["q"].lower().split()]
    hits = []
    for r in RECORDS:
        text = (r["name"] + " " + r["description"]).lower()
        if r["status"] == "APPROVED" and any(
                w in text for w in words if len(w) > 2):
            hits.append(r)
    return {"records": hits}


def records(q):  # the full catalog, for the admin view
    return {"records": RECORDS}


ROUTES = {"/approve": approve, "/search": search,
          "/records": records}


class Registry(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path not in ROUTES:
            page = (HERE / "page.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        body = json.dumps(ROUTES[url.path](q)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print("Registry on http://localhost:4051")
HTTPServer(("localhost", 4051), Registry).serve_forever()
