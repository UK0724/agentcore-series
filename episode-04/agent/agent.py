# The agent knows only ONE address: the gateway's /mcp endpoint.
# It never talks to the sprint API or the team API directly.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.gemini import GeminiModel
from strands.tools.mcp.mcp_client import MCPClient

GATEWAY = "http://localhost:4000/mcp"
GATEWAY_LOG = "http://localhost:4000/log"
HERE = Path(__file__).parent
PROMPT = ("You are a sprint assistant. Use your tools. "
          "Answer in one or two sentences.")


def rest_call_for(use):
    # Find the REST call the gateway made for this tool call.
    log = json.loads(urlopen(GATEWAY_LOG).read())
    return next(s for s in reversed(log)
                if s["tool"] == use["name"]
                and s["arguments"] == use["input"])


def run(question, send):
    gateway = MCPClient(
        lambda: streamable_http_client(GATEWAY))
    with gateway:
        # MCP tools/list, through the gateway
        tools = gateway.list_tools_sync()
        send("gateway", "The agent asked the gateway for tools",
             [t.tool_name for t in tools])

        asked = {}  # toolUseId -> the tool call the model asked for

        def on_event(**event):
            message = event.get("message") or {}
            for block in message.get("content", []):
                if "toolUse" in block:
                    use = block["toolUse"]
                    asked[use["toolUseId"]] = use
                    send("model", "The model asked for a tool",
                         {"tool": use["name"],
                          "input": use["input"]})
                elif "toolResult" in block:
                    use_id = block["toolResult"]["toolUseId"]
                    step = rest_call_for(asked[use_id])
                    send("rest", "The gateway made a REST call",
                         {"rest": step["rest"],
                          "response": step["response"]})
                elif ("text" in block
                      and message["role"] == "assistant"):
                    send("answer", "The model answered",
                         block["text"])

        key = os.environ["GOOGLE_API_KEY"]
        model = GeminiModel(client_args={"api_key": key},
                            model_id="gemini-flash-lite-latest")
        agent = Agent(model=model, tools=tools,
                      system_prompt=PROMPT,
                      callback_handler=on_event)
        agent(question)


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


print("Agent page on http://localhost:3012")
ThreadingHTTPServer(("localhost", 3012), Page).serve_forever()
