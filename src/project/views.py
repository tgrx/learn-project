import json
from datetime import datetime
from pathlib import Path

from django.http import HttpResponse


def handle_goodbye(request):
    hour = datetime.now().hour
    tod = "dias" if hour in range(6, 16) else "noches"
    msg = f"Buenos {tod}"
    return HttpResponse(msg)


def handle_projects(req, **kwargs):
    projects_file = Path(__file__).parent.parent.parent / "projects.json"
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
