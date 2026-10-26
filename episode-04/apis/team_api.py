# A second, separate REST API: who is who, on port 4002.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PEOPLE = {
    "priya": {"name": "Priya", "team": "Web", "onCall": True},
    "arjun": {"name": "Arjun", "team": "Data", "onCall": False},
}


class TeamApi(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")  # /people/priya
        known = len(parts) == 2 and parts[0] == "people"
        if known and parts[1] in PEOPLE:
            body, status = PEOPLE[parts[1]], 200
        else:
            body, status = {"error": "not found"}, 404
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


HTTPServer(("localhost", 4002), TeamApi).serve_forever()
