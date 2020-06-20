import os
import socketserver
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from typing import Dict
from typing import Union
from urllib.parse import parse_qs
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

TEMPLATES_DIR = PROJECT_DIR / "templates"
print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    ...


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.extract_path()
        handlers = {
            "/hello": self.handle_hello,
            "/goodbye": self.handle_goodbye,
            "/projects": self.handle_projects,
            "/resume": self.handle_resume,
        }

        default_handler = super().do_GET

        handler = handlers.get(path, default_handler)
        try:
            handler()
        except NotFound:
            self.respond_404()
        except MethodNotAllowed:
            self.respond_405()

    def handle_projects(self):
        html = TEMPLATES_DIR / "projects" / "index.html"
        contents = self.get_file_contents(html)
        self.respond(contents, "text/html")

    def handle_resume(self):
        html = TEMPLATES_DIR / "resume" / "index.html"
        contents = self.get_file_contents(html)
        self.respond(contents, "text/html")

    def get_file_contents(self, fp: Path) -> str:
        if not fp.is_file():
            raise NotFound

        with fp.open("r") as src:
            ct = src.read()
        
        return ct

    def handle_hello(self) -> None:
        raise MethodNotAllowed

        args = self.build_query_args()
        name = self.build_name(args)
        age = self.build_age(args)

        msg = f"Hello {name}!"
        if age is not None:
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
        path, *_rest = self.path.split("?")
        path, *_rest = path.split("#")
        if path[-1] == "/":
            path = path[:-1]
        return path

    def build_name(self, query_args: Dict) -> str:
        return query_args.get("name", "Anonymous")

    def build_age(self, query_args: Dict) -> Union[int, None]:
        age = query_args.get("age")
        if age is None:
            return age
        return int(age)

    def respond(self, msg: str, content_type="text/plain") -> None:
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())

    def respond_404(self) -> None:
        msg = "Ooops! Nothing found!"
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())

    def respond_405(self) -> None:
        msg = "Method Not Allowed"
        self.send_response(405)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it" + " works")
    httpd.serve_forever()
