# A pretend calendar service (like Google Calendar), port 4011.
# It only answers when the request carries a valid access token.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import jwt

# The calendar's own signing secret. Only the token vault knows it.
SECRET = "calendar-demo-secret-not-real-0001"
MEETINGS = {"uday": ["10:00 Sprint-42 standup", "15:00 Bug triage"]}


class CalendarApi(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization", "")
        try:
            claims = jwt.decode(auth.removeprefix("Bearer "), SECRET,
                                algorithms=["HS256"])
            body = {"user": claims["sub"],
                    "meetings": MEETINGS.get(claims["sub"], [])}
            status = 200
        except jwt.PyJWTError:
            body, status = {"error": "missing or bad token"}, 401
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


HTTPServer(("localhost", 4011), CalendarApi).serve_forever()
