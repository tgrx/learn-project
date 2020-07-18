import json
from datetime import datetime

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from project.utils import build_age
from project.utils import build_name
from project.utils import build_query_args
from project.utils import get_static_content
from project.utils import load_user_session

TEMPLATES_DIR = settings.REPO_DIR / "templates"


@require_http_methods(["GET", "POST"])
def handle_hello(req: HttpRequest):
    handlers = {
        "GET": handle_hello_get,
        "POST": handle_hello_post,
    }

    handler = handlers[req.method]
    return handler(req)


def handle_hello_get(req):
    session = load_user_session(req) or build_query_args(req)
    name = build_name(session)
    age = build_age(session)

    year = None
    if age is not None:
        year = datetime.now().year - age

    html_form = get_static_content(TEMPLATES_DIR / "hello" / "form.html")
    html_index = get_static_content(TEMPLATES_DIR / "hello" / "index.html")
    html_base = get_static_content(TEMPLATES_DIR / "base.html")

    html = html_index.format(form=html_form, name=name, birth_year=year)
    html = html_base.format(title="Hello!", body=html)

    return HttpResponse(html)


def handle_hello_post(req: HttpRequest):
    return redirect("/goodbye/")


@require_http_methods(["GET"])
def handle_goodbye(request: HttpRequest):
    hour = datetime.now().hour
    tod = "dias" if hour in range(6, 16) else "noches"
    msg = f"Buenos {tod}"
    return HttpResponse(msg)


def handle_lesson(req: HttpRequest):
    lesson_file = settings.REPO_DIR / "lessons" / "02.txt"
    with lesson_file.open("r") as fp:
        return HttpResponse(fp.read(), content_type="text/plain")


def handle_projects(req: HttpRequest, **kwargs):
    projects_file = settings.REPO_DIR / "projects.json"
    with projects_file.open("r") as fp:
        projects = json.load(fp)

    html = "<ul>"

    for proj_id, proj in projects.items():
        html += f"<li>{proj}</li>"

    html += "</ul>"
    html += "<hr>"
    project_id = kwargs.get("project_id")
    html += f"<h1>Project: {project_id}</h1>"
    html += "<hr>"

    return HttpResponse(html)
