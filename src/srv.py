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

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

PROJECT_DIR = Path(__file__).parent.parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

TEMPLATES_DIR = PROJECT_DIR / "templates"
print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")

USER_SESSIONS = PROJECT_DIR / "sessions.json"
print(f"USER_SESSIONS = {USER_SESSIONS}")


class AppError(RuntimeError):
    pass


class NotFound(AppError):
    pass


class MethodNotAllowed(AppError):
    ...


class UnknownPath(AppError):
    pass


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.do("get")
        except UnknownPath:
            super().do_GET()

    def do_POST(self):
        try:
            self.do("post")
        except UnknownPath:
            super().do_POST()

    def do(self, method: str):
        handlers = {
            "/hello": self.handle_hello,
            "/goodbye": self.handle_goodbye,
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
            self.respond_404()
        except MethodNotAllowed:
            self.respond_405()
        except Exception:
            self.respond_500()
            traceback.print_exc()

    def handle_projects(self, method: str):
        html = TEMPLATES_DIR / "projects" / "index.html"
        contents = self.get_file_contents(html)
        self.respond(contents)

    def handle_resume(self, method: str):
        html = TEMPLATES_DIR / "resume" / "index.html"
        contents = self.get_file_contents(html)
        self.respond(contents)

    def get_file_contents(self, fp: Path) -> str:
        if not fp.is_file():
            raise NotFound

        with fp.open("r") as src:
            ct = src.read()

        return ct

    def handle_hello(self, method: str) -> None:
        if method == "post":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            form = self.build_form(data)
            sessions = self.load_user_sessions()
            sessions.update(form)
            self.save_user_sessions(sessions)
            self.respond_302("/")
            return

        try:
            with USER_SESSIONS.open("r") as fp:
                args = json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            args = self.build_query_args()

        name = self.build_name(args)
        age = self.build_age(args)

        msg = f"Hello {name}!"
        if age is not None:
            year = datetime.now().year - age
            msg += f"\n\nYou was born at {year}."

        msg += f"""
        <form method="post">
        <p>
        <label for="name">Name:</label>
        <input id="name" name="name"></input>
        </p>
        <p>
        <label for="age">Age:</label>
        <input id="age" name="age"></input>
        </p>
        <button type="submit">Send</button>
        </form>
        """

        self.respond(msg)

    def handle_goodbye(self, method: str) -> None:
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

    def build_form(self, data: bytes) -> Dict[str, str]:
        payload = data.decode()
        qs = parse_qs(payload)
        form = {}
        for key, values in qs.items():
            if not values:
                continue
            form[key] = values[0]

        return form

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

    def respond_404(self) -> None:
        msg = "Ooops! Nothing found!"
        self._respond(404, msg, {"Content-Type": "text/plain"})

    def respond_405(self) -> None:
        msg = "Method Not Allowed"
        self._respond(405, msg, {"Content-Type": "text/plain"})

    def respond_500(self) -> None:
        hdr = "Internal Server Error"
        exc = traceback.format_exc()
        msg = f"{hdr}\n\n{exc}"
        self._respond(500, msg, {"Content-Type": "text/plain"})

    def respond_302(self, redirect_to: str):
        self._respond(302, None, {"Location": redirect_to})

    def respond(
        self,
        msg: str,
        headers: Optional[Dict] = None,
        content_type: Optional[str] = None,
    ) -> None:
        actual_headers = headers or {}
        actual_headers = {h.upper(): v for h, v in actual_headers.items()}
        actual_headers.update({"CONTENT-LENGTH": str(len(msg))})
        actual_headers.update({"CACHE-CONTROL": f"max-age={30 * 24 * 60 * 60}"})

        if content_type or "CONTENT-TYPE" not in actual_headers:
            actual_headers["CONTENT-TYPE"] = content_type or "text/html"

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

    def load_user_sessions(self) -> Dict:
        try:
            with USER_SESSIONS.open("r") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_user_sessions(self, sessions: Dict) -> None:
        with USER_SESSIONS.open("w") as fp:
            json.dump(sessions, fp)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)
