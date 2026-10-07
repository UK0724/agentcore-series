# A local stand-in for a managed harness: read the config, let Strands run the loop,
# and send every loop event to the page as a card.
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from strands import Agent
from strands.models.gemini import GeminiModel

from tools import ALL_TOOLS

HERE = Path(__file__).parent
CONFIG = json.loads((HERE / "harness.json").read_text())


def build_agent(callback):
    # 1. The model, from the config.
    model = GeminiModel(
        client_args={"api_key": os.environ["GOOGLE_API_KEY"]},
        model_id=CONFIG["model"]["modelId"],
    )
    # 2. The instructions and the tools, from the config.
    return Agent(
        model=model,
        system_prompt=CONFIG["systemPrompt"],
        tools=[ALL_TOOLS[name] for name in CONFIG["tools"]],
        callback_handler=callback,
    )


def cards_from(send):
    # Strands calls this for every event in the loop. We keep the complete messages.
    def callback(**event):
        message = event.get("message")
        if not message:
            return
        for block in message["content"]:
            if "toolUse" in block:
                use = block["toolUse"]
                send("model", "The model asked for a tool (stop reason: tool_use)",
                     {"tool": use["name"], "input": use["input"]})
            elif "toolResult" in block:
                result = block["toolResult"]["content"][0]
                data = result.get("json") or json.loads(result["text"])
                send("tool", "The loop ran the tool and sent back the result", data)
            elif "text" in block and message["role"] == "assistant":
                send("answer", "The model answered (stop reason: end_turn)",
                     block["text"])
    return callback


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/ask":
            page = (HERE / "page" / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()

        def send(who, title, data):
            card = json.dumps({"who": who, "title": title, "data": data})
            self.wfile.write(f"data: {card}\n\n".encode())
            self.wfile.flush()

        question = parse_qs(url.query)["q"][0]
        send("loop", "The loop sent the question, instructions and tools to the model",
             {"model": CONFIG["model"]["modelId"], "tools": CONFIG["tools"]})
        try:
            build_agent(cards_from(send))(question)
        except Exception as error:
            send("error", "Something failed", str(error))
        self.wfile.write(b"event: done\ndata: end\n\n")


print("Local harness demo on http://localhost:3010")
ThreadingHTTPServer(("localhost", 3010), Handler).serve_forever()
