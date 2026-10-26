# The optimization loop on one page, port 3022:
# 1. recommend a better prompt, 2. save it as config bundle v2,
# 3. A/B test v1 against v2, 4. keep the winner.
import json
import sys
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent / "agent"))
from ab_test import TRAFFIC, run_session  # noqa: E402
from recommend import recommend  # noqa: E402

BUNDLES = HERE / "bundles.json"
FAILURE = ("Q: How hot is it in Paris today? A: It is 22 degrees "
           "in Paris. Judge: 1 of 5, the number was made up.")


def new_recommendation():
    bundles = json.loads(BUNDLES.read_text())
    better = recommend(bundles["v1"]["systemPrompt"], FAILURE)
    bundles["v2"] = {"systemPrompt": better, "basedOn": "v1",
                     "model": bundles["v1"]["model"]}
    BUNDLES.write_text(json.dumps(bundles, indent=2))  # versioned
    return bundles


class Page(BaseHTTPRequestHandler):
    def reply(self, kind, body):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/recommend":
            body = json.dumps(new_recommendation()).encode()
            return self.reply("application/json", body)
        if self.path != "/abtest":
            page = (HERE / "index.html").read_bytes()
            return self.reply("text/html", page)
        bundles = json.loads(BUNDLES.read_text())
        prompts = {"A": bundles["v1"]["systemPrompt"],
                   "B": bundles["v2"]["systemPrompt"]}
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        for n, question in enumerate(TRAFFIC, start=1):
            row = run_session(f"session-{n}", question, prompts)
            self.wfile.write(f"data: {json.dumps(row)}\n\n".encode())
            self.wfile.flush()
        self.wfile.write(b"event: done\ndata: end\n\n")


print("Optimization page on http://localhost:3022")
ThreadingHTTPServer(("localhost", 3022), Page).serve_forever()
