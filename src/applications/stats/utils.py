from delorean import Delorean
from django.http import HttpRequest
from django.http import HttpResponse

from applications.stats.models import Visit


def count_stats(view):
    class ViewWithStats(view):
        def dispatch(self, *args, **kwargs):
            t0 = Delorean()
            code = 500
            clen = 0
            try:
                resp: HttpResponse = super().dispatch(*args, **kwargs)
                code = resp.status_code
                try:
                    resp.render()
                    clen = len(resp.content)
                except AttributeError:
                    pass

                return resp
            finally:
                td = Delorean() - t0
                count_visit(self.request, code, td.total_seconds(), clen)

    return ViewWithStats


def count_visit(request: HttpRequest, code: int, timing: float, content_length: int):
    one_kb = 2 ** 10
    ms_in_s = 1000

    visit = Visit(
        at=Delorean().datetime,
        cl=content_length / one_kb,
        code=code,
        method=request.method,
        tm=timing * ms_in_s,
        url=request.path,
    )
    visit.save()
