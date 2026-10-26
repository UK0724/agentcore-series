# A website with NO API, port 4031: a parcel tracking page.
# The only way in is to use it like a person: type and click.
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PARCELS = {"ORD-7": "Out for delivery, arriving by 6 pm today"}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>QuickShip tracking</title>
<style>body{{font:28px system-ui;margin:60px;background:#fffdf5}}
input,button{{font:inherit;padding:10px}} .status{{margin-top:30px;
font-size:34px;color:#1b5e20}}</style></head><body>
<h1>QuickShip parcel tracking</h1>
<form action="/track"><label>Order number
<input name="order"></label> <button>Track</button></form>
<div class="status">{status}</div></body></html>"""


class Site(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        order = parse_qs(url.query).get("order", [""])[0]
        status = ""
        if order:
            status = PARCELS.get(order, "No parcel found")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(PAGE.format(status=status).encode())


HTTPServer(("localhost", 4031), Site).serve_forever()
