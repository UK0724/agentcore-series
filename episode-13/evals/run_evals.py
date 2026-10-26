# Runs every test case through the agent, then scores it three
# ways: did it use the tool, is the expected fact in the answer,
# and what does the LLM judge say. Page on port 3021.
import json
import sys
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path

from judge import judge

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent / "agent"))
from weather_agent import make_agent  # noqa: E402

CASES = json.loads((HERE / "cases.json").read_text())


def evaluate(case, version):
    result = make_agent(version)(case["input"])
    answer = str(result).strip()
    used_tool = "get_weather" in result.metrics.tool_metrics
    has_fact = case["expected"].lower() in answer.lower()
    score, reason = judge(case["input"], answer, case["rubric"])
    return {"input": case["input"], "answer": answer,
            "tool": used_tool, "fact": has_fact,
            "score": score, "reason": reason,
            "passed": used_tool and has_fact and score >= 4}


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith("/run"):
            page = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        version = self.path.split("=")[-1]  # /run?v=v1
        for case in CASES:
            row = json.dumps(evaluate(case, version))
            self.wfile.write(f"data: {row}\n\n".encode())
            self.wfile.flush()
        self.wfile.write(b"event: done\ndata: end\n\n")


print("Evaluations page on http://localhost:3021")
ThreadingHTTPServer(("localhost", 3021), Page).serve_forever()
