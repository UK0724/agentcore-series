# An agent with web search. On AWS the tool comes from a Gateway
# connector; here it is our pretend search. Port 3023.
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from strands import Agent
from strands.models.gemini import GeminiModel

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent / "search"))
from web_search import web_search  # noqa: E402

PROMPT = ("Answer using web_search. Cite every source URL you use. "
          "Answer in two short sentences, then list the sources.")


def run(question, send):
    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    agent = Agent(model=model, tools=[web_search],
                  system_prompt=PROMPT, callback_handler=None)
    result = agent(question)
    for message in agent.messages:  # find the searches in the log
        for block in message["content"]:
            if "toolUse" in block:
                send("search", "Searched the web",
                     block["toolUse"]["input"])
            if "toolResult" in block:
                part = block["toolResult"]["content"][0]
                data = part.get("json") or json.loads(part["text"])
                send("results", "Search results", data)
    send("answer", "The model answered", str(result).strip())


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/ask":
            page = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()

        def send(who, title, data):
            card = {"who": who, "title": title, "data": data}
            line = f"data: {json.dumps(card)}\n\n"
            self.wfile.write(line.encode())
            self.wfile.flush()

        try:
            run(parse_qs(url.query)["q"][0], send)
        except Exception as error:
            send("error", "Something failed", str(error))
        self.wfile.write(b"event: done\ndata: end\n\n")


print("Agent page on http://localhost:3023")
ThreadingHTTPServer(("localhost", 3023), Page).serve_forever()
