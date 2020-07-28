from datetime import datetime

from django.http import HttpRequest
from django.http import HttpResponse

from applications.stats.models import Visit


def count_stats(view):
    class ViewWithStats(view):
        def dispatch(self, *args, **kwargs):
            t0 = datetime.now()
            code = 500
            try:
                resp: HttpResponse = super().dispatch(*args, **kwargs)
                code = resp.status_code
                return resp
            finally:
                td = datetime.now() - t0
                count_visit(self.request, code, td.total_seconds() * 1000.0)

    return ViewWithStats


def count_visit(request: HttpRequest, code: int, timing: float):
    visit = Visit(
        at=datetime.now(),
        code=code,
        method=request.method,
        tm=timing,
        url=request.path,
    )
    visit.save()
