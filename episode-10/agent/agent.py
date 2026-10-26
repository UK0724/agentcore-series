# An agent that finds help through the registry: it searches the
# catalog, and only ever sees records that were approved.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

from strands import Agent, tool
from strands.models.gemini import GeminiModel

REGISTRY = "http://localhost:4051"
PROMPT = ("Find who can help by searching the company registry "
          "with one or two keywords. Answer in one sentence, "
          "naming the record. If nothing matches, say so.")


def run(question, send):
    @tool
    def search_registry(query: str) -> dict:
        """Search the company registry of agents and tools."""
        with urlopen(f"{REGISTRY}/search?q={quote(query)}") as r:
            result = json.loads(r.read())
        names = [x["name"] for x in result["records"]]
        send("search", f"Searched the registry for: {query}", names)
        return result

    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    agent = Agent(model=model, tools=[search_registry],
                  system_prompt=PROMPT, callback_handler=None)
    send("answer", "The model answered", str(agent(question)).strip())


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Access-Control-Allow-Origin", "*")
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


print("Agent on http://localhost:3018")
ThreadingHTTPServer(("localhost", 3018), Page).serve_forever()
