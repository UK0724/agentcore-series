# Short-term memory: Strands keeps each session's turns in files.
# Long-term memory: facts extracted from a session, kept per user.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from strands import Agent
from strands.models.gemini import GeminiModel
from strands.session.file_session_manager import FileSessionManager

import long_term

HERE = Path(__file__).parent
SESSIONS = HERE / "memory" / "sessions"
PROMPT = "You are a friendly sprint assistant. Answer briefly."


def model():
    key = os.environ["GOOGLE_API_KEY"]
    return GeminiModel(client_args={"api_key": key},
                       model_id="gemini-flash-lite-latest")


def chat(actor_id, session_id, message):
    # Long-term: retrieve facts about this user, add to the prompt.
    facts = long_term.retrieve(actor_id, message)
    prompt = PROMPT
    if facts:
        prompt += " Known facts about the user: " + "; ".join(facts)
    # Short-term: the session manager reloads this session's turns.
    sessions = FileSessionManager(session_id=session_id,
                                  storage_dir=str(SESSIONS))
    agent = Agent(model=model(), system_prompt=prompt,
                  session_manager=sessions, callback_handler=None)
    reply = str(agent(message)).strip()
    turns = [m["content"][0].get("text", "") for m in agent.messages]
    return {"reply": reply, "facts_used": facts, "turns": turns}


def extract(actor_id, session_id):
    # Read the whole session, and ask the model for lasting facts.
    sessions = FileSessionManager(session_id=session_id,
                                  storage_dir=str(SESSIONS))
    agent = Agent(model=model(), session_manager=sessions,
                  callback_handler=None)
    talk = "\n".join(f"{m['role']}: {m['content'][0].get('text', '')}"
                     for m in agent.messages)
    ask = ("List lasting facts about the user from this chat, "
           "one per line, no bullets:\n" + talk)
    fresh = Agent(model=model(), callback_handler=None)
    facts = [f.strip() for f in str(fresh(ask)).splitlines()
             if f.strip()]
    return {"saved": long_term.save_records(actor_id, facts)}


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        if url.path == "/chat":
            body = chat(q["actor"], q["session"], q["message"])
        elif url.path == "/extract":
            body = extract(q["actor"], q["session"])
        else:
            page = (HERE / "page.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


print("Memory demo on http://localhost:3013")
ThreadingHTTPServer(("localhost", 3013), Page).serve_forever()
