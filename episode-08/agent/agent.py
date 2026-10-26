# An agent with browser tools. The browser runs in a separate,
# isolated service; the agent only sends it simple actions.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import urlopen

from strands import Agent, tool
from strands.models.gemini import GeminiModel

HERE = Path(__file__).parent
BROWSER = "http://localhost:4032"
PROMPT = ("You can use a web browser. The tracking site is "
          "http://localhost:4031. Answer in one sentence.")


def browser_call(action, **params):
    with urlopen(f"{BROWSER}/{action}?{urlencode(params)}") as r:
        return json.loads(r.read())


def run(question, send):
    session = browser_call("start")["session"]
    send("session", "Started an isolated browser session", session)

    def act(action, title, **params):
        result = browser_call(action, session=session, **params)
        send("browser", title, result)
        return {k: v for k, v in result.items() if k != "screenshot"}

    @tool
    def open_page(url: str) -> dict:
        """Open a web page in the browser."""
        return act("goto", f"Opened {url}", url=url)

    @tool
    def type_text(field: str, text: str) -> dict:
        """Type text into the input with this label."""
        return act("type", f"Typed {text}", field=field, text=text)

    @tool
    def click_button(button: str) -> dict:
        """Click the button with this name."""
        return act("click", f"Clicked {button}", button=button)

    @tool
    def read_page() -> dict:
        """Read all the text on the current page."""
        return act("read", "Read the page")

    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    tools = [open_page, type_text, click_button, read_page]
    agent = Agent(model=model, tools=tools, system_prompt=PROMPT,
                  callback_handler=None)
    send("answer", "The model answered", str(agent(question)).strip())


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


print("Agent page on http://localhost:3016")
ThreadingHTTPServer(("localhost", 3016), Page).serve_forever()
