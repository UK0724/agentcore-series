# A normal REST API, nothing to do with AI: sprint data on port 4001.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SPRINTS = {
    "sprint-42": {
        "velocity": 38,
        "daysLeft": 3,
        "blockingBugs": [
            {"id": "BUG-311", "owner": "priya"},
            {"id": "BUG-318", "owner": "arjun"},
        ],
    },
}


class SprintApi(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")  # /sprints/sprint-42
        known = len(parts) == 2 and parts[0] == "sprints"
        if known and parts[1] in SPRINTS:
            body, status = SPRINTS[parts[1]], 200
        else:
            body, status = {"error": "not found"}, 404
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


HTTPServer(("localhost", 4001), SprintApi).serve_forever()
