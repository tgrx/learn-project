import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from typing import Dict
from urllib.parse import parse_qs

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello"):
            return self.handle_hello()
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def handle_hello(self):
        args = self.build_query_args()
        name = args.get("name", "Anonymous")
        msg = f"Hello {name}!"
        self.respond(msg)

    def build_query_args(self) -> Dict:
        _path, *qs = self.path.split("?")
        args = {}

        if len(qs) != 1:
            return args

        qs = qs[0]
        qs = parse_qs(qs)

        for key, values in qs.items():
            if not values:
                continue
            args[key] = values[0]

        return args

    def respond(self, msg: str):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()
