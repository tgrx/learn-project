import json
import os
import re
import socketserver
import traceback
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Tuple
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
PROJECTS = PROJECT_DIR / "projects.json"
DEBUG = True

print("*" * 80)
print(f"PORT = {PORT}")
print(f"PROJECT_DIR = {PROJECT_DIR}")
print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")
print(f"USER_SESSIONS = {USER_SESSIONS}")
print(f"DEBUG = {DEBUG}")
print("*" * 80)
print(f"URL: http://localhost:{PORT}/")
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
            r"^$": self.handle_index,
            r"^/goodbye$": self.handle_goodbye,
            r"^/hello$": self.handle_hello,
            r"^/project(/(?P<project_id>\w+))$": self.handle_projects,
            r"^/project/(?P<project_id>\w+)/(?P<update>update)$": self.handle_projects_add,
            r"^/project/(?P<project_id>\w+)/delete$": self.handle_project_delete,
            r"^/projects$": self.handle_projects,
            r"^/projects/add$": self.handle_projects_add,
            r"^/resume$": self.handle_resume,
        }

        path = self.extract_path()
        handler, kwargs = self.get_handler(handlers, path)

        try:
            handler(method, **kwargs)
        except NotFound:
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()
            traceback.print_exc()

    @staticmethod
    def get_handler(handlers, path) -> Tuple:
        handler = None
        kwargs = {}

        for pattern, registered_handler in handlers.items():
            match = re.match(pattern, path)
            if not match:
                continue

            handler = registered_handler
            kwargs = match.groupdict().copy()
            break

        if not handler:
            raise UnknownPath(path)

        return handler, kwargs

    def handle_index(self, method: str, **kwargs):
        template = TEMPLATES_DIR / "index.html"
        html_template = get_static_content(template)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Learn Project", body=html_template)
        self.respond(html)

    def handle_projects(self, method: str, **kwargs):
        template = TEMPLATES_DIR / "projects" / "index.html"
        html_template = get_static_content(template)
        project_id = kwargs.get("project_id")
        projects = self.render_projects(project_id)
        html_template = html_template.format(projects=projects)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Projects :: Learn Project", body=html_template)
        self.respond(html)

    def render_projects(self, project_id: Optional[str] = None) -> str:
        if project_id:
            return self.render_single_project(project_id)

        projects = self.load_projects_file()
        projects_str = "<ul>"
        for existing_project_id, project in projects.items():
            name = project["name"]
            start = project["start"]
            end = project.get("end", "now")
            link = f'<a href="/project/{existing_project_id}">{name}</a>'
            projects_str += f"<li>{link}: from {start} till {end}</li>"
        projects_str += "</ul>"
        return projects_str

    def render_single_project(self, project_id: str) -> str:
        projects = self.load_projects_file()
        try:
            project = projects[project_id]
        except KeyError:
            raise NotFound

        name = project["name"]
        start = project["start"]
        end = project.get("end", "now")

        html = get_static_content(TEMPLATES_DIR / "projects" / "add.html")
        html = html.format(
            value_action=f"/project/{project_id}/update/",
            value_end=end,
            value_name=name,
            value_start=start,
            value_submit="Update",
        )

        html += f"""
        <form method="post" action="/project/{project_id}/delete/">
            <button type="submit">Delete project</button>
        </form>
        """

        return html

    def handle_projects_add(self, method: str, **kwargs):
        handlers = {
            "get": self.handle_projects_add_get,
            "post": self.handle_projects_add_post,
        }
        try:
            handler = handlers[method]
            return handler(**kwargs)
        except KeyError:
            raise MethodNotAllowed

    def handle_projects_add_get(self, **kwargs):
        html = get_static_content(TEMPLATES_DIR / "projects" / "add.html")
        html = html.format(
            value_action="/projects/add/",
            value_name="",
            value_start="",
            value_end="",
            value_submit="Add",
        )
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Projects :: Add Project", body=html)
        self.respond(html)

    def handle_projects_add_post(self, **kwargs):
        form = self.get_form()
        redirect = partial(self.redirect, "/projects/")

        if not form:
            redirect()

        projects = self.load_projects_file()

        if kwargs.get("update") == "update":
            project_id = kwargs.get("project_id")
            if not project_id:
                raise NotFound

            project = projects.get(project_id, form)
            project.update(form)
        else:
            project_id = os.urandom(16).hex()
            project = form

        projects.update({project_id: project})
        self.save_projects_file(projects)

        redirect()

    def handle_project_delete(self, method: str, **kwargs):
        if method != "post":
            raise MethodNotAllowed

        projects = self.load_projects_file()

        project_id = kwargs.get("project_id")
        if not project_id:
            raise NotFound

        try:
            del projects[project_id]
        except KeyError:
            pass

        self.save_projects_file(projects)

        self.redirect("/projects/")

    def handle_resume(self, method: str, **kwargs):
        template = TEMPLATES_DIR / "resume" / "index.html"
        html_template = get_static_content(template)
        html_base = get_static_content(TEMPLATES_DIR / "base.html")
        html = html_base.format(title="Resume :: Learn Project", body=html_template)
        self.respond(html)

    def handle_hello(self, method: str, **kwargs) -> None:
        handlers = {
            "get": self.handle_hello_get,
            "post": self.handle_hello_post,
        }
        try:
            handler = handlers[method]
            return handler()
        except KeyError:
            raise MethodNotAllowed

    def handle_hello_get(self, **kwargs) -> None:
        session = self.load_user_session() or self.build_query_args()
        name = self.build_name(session)
        age = self.build_age(session)

        year = None
        if age is not None:
            year = datetime.now().year - age

        html_form = get_static_content(TEMPLATES_DIR / "hello" / "form.html")
        html_index = get_static_content(TEMPLATES_DIR / "hello" / "index.html")
        html_base = get_static_content(TEMPLATES_DIR / "base.html")

        html = html_index.format(form=html_form, name=name, birth_year=year)
        html = html_base.format(title="Hello!", body=html)

        self.respond(html)

    def handle_hello_post(self, **kwargs) -> None:
        form = self.get_form()
        session = self.load_user_session()
        session.update(form)
        session_id = self.save_user_session(session)
        self.redirect("/", headers={"Set-Cookie": f"SID={session_id}; Max-Age=120"})

    def get_session_id(self) -> Union[str, None]:
        cookie = self.headers.get("Cookie")
        if not cookie:
            return None

        qs, *_extra = cookie.split(";")
        args = linearize_qs(parse_qs(qs))
        session_id = args.get("SID")
        return session_id

    def load_user_session(self) -> Dict:
        session_id = self.get_session_id()
        if not session_id:
            return {}

        sessions = self.load_sessions_file()
        return sessions.get(session_id, {})

    def save_user_session(self, session: Dict) -> str:
        session_id = self.get_session_id() or os.urandom(16).hex()
        sessions = self.load_sessions_file()
        sessions[session_id] = session
        self.save_sessions_file(sessions)

        return session_id

    def load_sessions_file(self) -> Dict:
        try:
            with USER_SESSIONS.open("r") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_sessions_file(self, sessions):
        with USER_SESSIONS.open("w") as fp:
            json.dump(sessions, fp)

    def load_projects_file(self) -> Dict:
        try:
            with PROJECTS.open("r") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_projects_file(self, projects) -> None:
        with PROJECTS.open("w") as fp:
            json.dump(projects, fp)

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

    def redirect(self, redirect_to: str, headers: Optional[Dict] = None):
        actual_headers = {h("location"): redirect_to}
        if headers:
            actual_headers.update(headers)

        self._respond(302, None, actual_headers)

    def respond(
        self,
        msg: str,
        headers: Optional[Dict] = None,
        content_type: Optional[str] = None,
    ) -> None:
        actual_headers = headers or {}
        actual_headers = {h(header): value for header, value in actual_headers.items()}
        actual_headers.update({h("content-length"): str(len(msg))})
        # actual_headers.update({h("cache-control"): f"max-age={10 * 60}"})

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
