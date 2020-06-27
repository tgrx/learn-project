import json
import os
import socketserver
import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Union
from urllib.parse import parse_qs

from errors import MethodNotAllowed
from errors import NotFound
from errors import UnknownPath
from utils import get_static_content
from utils import h
from utils import linearize_qs

PORT = int(os.getenv("PORT", 8000))
PROJECT_DIR = Path(__file__).parent.parent.resolve()
TEMPLATES_DIR = PROJECT_DIR / "templates"
USER_SESSIONS = PROJECT_DIR / "sessions.json"
DEBUG = True

print("*" * 80)
print(f"PORT = {PORT}")
print(f"PROJECT_DIR = {PROJECT_DIR}")
print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")
print(f"USER_SESSIONS = {USER_SESSIONS}")
print(f"DEBUG = {DEBUG}")
print("*" * 80)


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.dispatch("get")
        except UnknownPath:
            self.handle_404()

    def do_POST(self):
        try:
            self.dispatch("post")
        except UnknownPath:
            self.handle_404()

    def dispatch(self, method: str):
        handlers = {
            "": self.handle_index,
            "/goodbye": self.handle_goodbye,
            "/hello": self.handle_hello,
            "/projects": self.handle_projects,
            "/resume": self.handle_resume,
        }
        path = self.extract_path()

        if path not in handlers:
            raise UnknownPath(path)

        handler = handlers[path]

        try:
            handler(method)
        except NotFound:
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()
            traceback.print_exc()

    def handle_index(self, method: str):
        template = TEMPLATES_DIR / "index.html"
        html_template = get_static_content(template)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Learn Project", body=html_template)
        self.respond(html)

    def handle_projects(self, method: str):
        template = TEMPLATES_DIR / "projects" / "index.html"
        html_template = get_static_content(template)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Projects :: Learn Project", body=html_template)
        self.respond(html)

    def handle_resume(self, method: str):
        template = TEMPLATES_DIR / "resume" / "index.html"
        html_template = get_static_content(template)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Resume :: Learn Project", body=html_template)
        self.respond(html)

    def handle_hello(self, method: str) -> None:
        handlers = {
            "get": self.handle_hello_get,
            "post": self.handle_hello_post,
        }
        try:
            handler = handlers[method]
            return handler()
        except KeyError:
            raise MethodNotAllowed

    def handle_hello_get(self) -> None:
        args = self.load_user_sessions() or self.build_query_args()
        name = self.build_name(args)
        age = self.build_age(args)

        year = None
        if age is not None:
            year = datetime.now().year - age

        html_form = get_static_content(TEMPLATES_DIR / "hello" / "form.html")
        html_index = get_static_content(TEMPLATES_DIR / "hello" / "index.html")
        html_base = get_static_content(TEMPLATES_DIR / "base.html")

        html = html_index.format(form=html_form, name=name, birth_year=year)
        html = html_base.format(title="Hello!", body=html)

        self.respond(html)

    def handle_hello_post(self) -> None:
        form = self.get_form()
        sessions = self.load_user_sessions()
        sessions.update(form)
        self.save_user_sessions(sessions)
        self.redirect("/")

    def handle_goodbye(self, method: str) -> None:
        hour = datetime.now().hour
        tod = "dias" if hour in range(9, 19) else "noches"
        msg = f"Buenos {tod}"
        self.respond(msg)

    def load_user_sessions(self) -> Dict:
        try:
            with USER_SESSIONS.open("r") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_user_sessions(self, sessions: Dict) -> None:
        with USER_SESSIONS.open("w") as fp:
            json.dump(sessions, fp)

    def build_query_args(self) -> Dict:
        _path, *qs = self.path.split("?")
        if len(qs) != 1:
            return {}

        qs = qs[0]
        qs = parse_qs(qs)
        args = linearize_qs(qs)

        return args

    def get_form(self) -> Dict[str, str]:
        payload = self.get_request_payload()
        qs = parse_qs(payload)
        form = linearize_qs(qs)

        return form

    def get_request_payload(self) -> str:
        try:
            content_length = int(self.headers[h("content-length")])
            payload = self.rfile.read(content_length)
        except (KeyError, ValueError):
            payload = ""

        return payload.decode()

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

    def handle_404(self) -> None:
        msg = "Ooops! Nothing found!"
        self._respond(404, msg, {h("content-type"): "text/plain"})

    def handle_405(self) -> None:
        msg = "Method Not Allowed"
        self._respond(405, msg, {h("content-type"): "text/plain"})

    def handle_500(self) -> None:
        hdr = "Internal Server Error"
        exc = traceback.format_exc() if DEBUG else ""
        msg = f"{hdr}\n\n{exc}"
        self._respond(500, msg, {h("content-type"): "text/plain"})

    def redirect(self, redirect_to: str):
        self._respond(302, None, {h("location"): redirect_to})

    def respond(
        self,
        msg: str,
        headers: Optional[Dict] = None,
        content_type: Optional[str] = None,
    ) -> None:
        actual_headers = headers or {}
        actual_headers = {h(header): value for header, value in actual_headers.items()}
        actual_headers.update({h("content-length"): str(len(msg))})
        actual_headers.update({h("cache-control"): f"max-age={10 * 60}"})

        if content_type or h("content-type") not in actual_headers:
            actual_headers[h("content-type")] = content_type or "text/html"

        self._respond(200, msg, actual_headers)

    def _respond(
        self,
        code: int,
        message: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict] = None,
    ) -> None:
        self.send_response(code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()

        if message:
            if isinstance(message, str):
                message = message.encode()

            self.wfile.write(message)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)
