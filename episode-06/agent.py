# The agent: it checks who is calling, and its calendar tool gets
# a short-lived token from the vault. No secret in this file.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from strands import Agent, tool
from strands.models.gemini import GeminiModel

import identity
from identity import requires_access_token

HERE = Path(__file__).parent


@requires_access_token("calendar")
def read_calendar(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    req = Request("http://localhost:4011/meetings", headers=headers)
    found = json.loads(urlopen(req).read())
    shown = ", ".join(found["meetings"])
    identity.EVENTS.append(("calendar", f"Token accepted: {shown}"))
    return found


def ask(user_token, question):
    user = identity.check_inbound(user_token)  # inbound auth

    @tool
    def get_my_meetings() -> dict:
        """Today's meetings of the signed-in user."""
        return read_calendar(user=user)  # outbound auth

    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    agent = Agent(model=model, tools=[get_my_meetings],
                  callback_handler=None,
                  system_prompt="Use your tools. Answer briefly.")
    return str(agent(question)).strip()


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        identity.EVENTS.clear()
        if url.path == "/sign-in":
            body = {"token": identity.sign_in(q["user"])}
        elif url.path == "/allow":
            identity.CONSENT.add((q["user"], "calendar"))
            body = {"allowed": "calendar"}
        elif url.path == "/ask":
            try:
                body = {"answer": ask(q.get("token", ""), q["q"])}
            except identity.ConsentNeeded:
                body = {"answer": "Please allow calendar access."}
            except Exception as error:
                body = {"answer": "Rejected: no valid sign-in token."}
        else:
            page = (HERE / "page.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        body["steps"] = identity.EVENTS[:]
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


print("Identity demo on http://localhost:3014")
ThreadingHTTPServer(("localhost", 3014), Page).serve_forever()
