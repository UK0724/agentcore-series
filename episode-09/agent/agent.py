# An agent that answers with code: it writes Python, the sandbox
# runs it, and the agent reads the output. No guessing at maths.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from strands import Agent, tool
from strands.models.gemini import GeminiModel

HERE = Path(__file__).parent
SANDBOX = "http://localhost:4041"
PROMPT = ("Always answer by running Python with run_python. "
          "The file sales.csv is in the working folder. "
          "Only the standard library is available, and each run "
          "starts fresh, so include imports. Print your results. "
          "Columns: day, orders, revenue. Solve it in one script. "
          "Answer in one or two sentences.")


def sandbox(action, **body):
    data = json.dumps(body).encode()
    request = Request(f"{SANDBOX}/{action}", data=data,
                      headers={"Content-Type": "application/json"})
    with urlopen(request) as r:
        return json.loads(r.read())


def run(question, send):
    session = sandbox("start")["session"]
    sandbox("upload", session=session, name="sales.csv")
    send("session", "Started a sandbox session", session)

    @tool
    def run_python(code: str) -> dict:
        """Run Python code in the sandbox and return its output."""
        send("code", "The model wrote this code", code)
        result = sandbox("run", session=session, code=code)
        send("output", "The sandbox ran it", result)
        return result

    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    agent = Agent(model=model, tools=[run_python],
                  system_prompt=PROMPT, callback_handler=None)
    answer = str(agent(question)).strip()
    sandbox("stop", session=session)  # always clean up
    send("answer", "The model answered", answer)


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


print("Agent page on http://localhost:3017")
ThreadingHTTPServer(("localhost", 3017), Page).serve_forever()
