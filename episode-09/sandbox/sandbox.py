# A tiny code sandbox service, port 4041, like AgentCore Code
# Interpreter: each session gets its own empty folder, and code
# runs in a separate Python process with a time limit.
# NOTE: a demo only. A real sandbox (AgentCore) isolates the
# whole machine; this just keeps code out of the agent process.
import json
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
sessions = {}  # session id -> its own working folder


def start(body):
    sid = f"session-{len(sessions) + 1}"
    folder = HERE / "sessions" / sid
    folder.mkdir(parents=True, exist_ok=True)
    sessions[sid] = folder
    return {"session": sid}


def upload(body):  # copy a data file into the session folder
    shutil.copy(DATA / body["name"], sessions[body["session"]])
    return {"uploaded": body["name"]}


def run(body):
    try:
        done = subprocess.run(
            [sys.executable, "-I", "-c", body["code"]],
            cwd=sessions[body["session"]],  # only sees its folder
            capture_output=True, text=True, timeout=10)
        return {"stdout": done.stdout, "stderr": done.stderr}
    except subprocess.TimeoutExpired:
        return {"stderr": "Stopped: ran longer than 10 seconds"}


def stop(body):  # the session folder is wiped
    shutil.rmtree(sessions.pop(body["session"]))
    return {"stopped": body["session"]}


ACTIONS = {"/start": start, "/upload": upload,
           "/run": run, "/stop": stop}


class Sandbox(BaseHTTPRequestHandler):
    def do_POST(self):
        size = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(size))
        result = ACTIONS[self.path](body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


print("Sandbox on http://localhost:4041")
HTTPServer(("localhost", 4041), Sandbox).serve_forever()
