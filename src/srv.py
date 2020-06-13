import os
import socketserver
from datetime import date
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from typing import Dict
from urllib.parse import parse_qs

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.extract_path()
        handlers = {
            "/hello": self.handle_hello,
            "/goodbye": self.handle_goodbye,
        }

        default_handler = super().do_GET

        handler = handlers.get(path, default_handler)
        handler()

    def handle_hello(self) -> None:
        args = self.build_query_args()
        name = self.build_name(args)
        age = self.build_age(args)

        msg = f"Hello {name}!"
        if age:
            year = datetime.now().year - age
            msg += f"\n\nYou was born at {year}."

        self.respond(msg)

    def handle_goodbye(self) -> None:
        hour = datetime.now().hour
        tod = "dias" if hour in range(9, 19) else "noches"
        msg = f"Buenos {tod}"
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

    def extract_path(self) -> str:
        return self.path.split("?")[0].split("#")[0]

    def build_name(self, query_args: Dict) -> str:
        return query_args.get("name", "Anonymous")

    def build_age(self, query_args: Dict) -> int:
        return int(query_args.get("age", 0))

    def respond(self, msg: str) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()
