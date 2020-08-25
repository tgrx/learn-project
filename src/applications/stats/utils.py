from datetime import timedelta
from itertools import product

from delorean import Delorean
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min
from django.http import HttpRequest
from django.http import HttpResponse
from django.template.response import TemplateResponse

from applications.stats.custom_types import DashboardT
from applications.stats.custom_types import HourlyT
from applications.stats.custom_types import MinMaxT
from applications.stats.models import Visit


def count_stats(view):
    class ViewWithStats(view):
        def dispatch(self, *args, **kwargs):
            t0 = Delorean()
            code = 500
            content_length = 0
            try:
                resp: HttpResponse = super().dispatch(*args, **kwargs)
                code = resp.status_code
                if isinstance(resp, TemplateResponse):
                    resp.render()
                content_length = len(bytes(resp))
                return resp
            finally:
                td = Delorean() - t0
                count_visit(self.request, code, td.total_seconds(), content_length)

    return ViewWithStats


def count_visit(request: HttpRequest, code: int, timing: float, content_length: int):
    one_kb = 2 ** 10
    ms_in_s = 1000

    visit = Visit(
        at=Delorean().datetime,
        cl=content_length,
        code=code,
        method=request.method,
        tm=timing * ms_in_s,
        url=request.path,
    )
    visit.save()


def generate_dashboard() -> DashboardT:
    dimensions = {"latency": "tm", "traffic": "cl"}
    aggregates = (Max, Min, Avg)

    select = {
        f"{dimension}_{aggregate.__name__.lower()}": aggregate(dimension)
        for aggregate, dimension in product(aggregates, dimensions.values())
    }

    ts_now = Delorean()
    params = {}

    for measure_attr, minutes in zip(HourlyT.__annotations__, (5, 15, 60, 60 * 24)):
        delta = timedelta(minutes=minutes)
        ts = (ts_now - delta).datetime

        query = Visit.objects.filter(at__gte=ts).aggregate(**select)

        for dimension_attr, dimension in dimensions.items():
            max_value = query[f"{dimension}_max"]
            min_value = query[f"{dimension}_min"]
            avg_value = query[f"{dimension}_avg"]

            metric = MinMaxT(min=min_value, max=max_value, avg=avg_value)
            params.setdefault(dimension_attr, {})[measure_attr] = metric

    dashboard = DashboardT(**params)

    return dashboard
