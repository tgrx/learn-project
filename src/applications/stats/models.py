from datetime import timedelta
from typing import NamedTuple
from typing import Optional

from delorean import Delorean
from django.db import models
from pandas import DataFrame

from project.utils import asdict


class MinMaxT(NamedTuple):
    max: float
    min: float
    avg: float


class HourlyT(NamedTuple):
    m05: MinMaxT
    m15: MinMaxT
    h01: MinMaxT
    h24: MinMaxT


class DashboardT(NamedTuple):
    latency: HourlyT
    traffic: HourlyT


class Visit(models.Model):
    at = models.DateTimeField(null=True, blank=True)
    cl = models.PositiveIntegerField(null=True, blank=True)
    code = models.PositiveIntegerField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    tm = models.FloatField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    @classmethod
    def generate_dashboard(cls) -> Optional[DashboardT]:
        df = DataFrame(map(asdict, Visit.objects.all()))
        if "at" not in df:
            return None

        try:
            del df["pk"]
        except KeyError:
            pass

        ts_now = Delorean()
        params = {}

        for measure_attr, minutes in zip(HourlyT.__annotations__, (5, 15, 60, 60 * 24)):
            delta = timedelta(minutes=minutes)
            ts = (ts_now - delta).datetime

            for dimension_attr, dimension in {"latency": "tm", "traffic": "cl"}.items():
                max_value = df.where(df["at"] >= ts).max()[dimension]
                min_value = df.where(df["at"] >= ts).min()[dimension]
                avg_value = df.where(df["at"] >= ts).mean()[dimension]

                metric = MinMaxT(min=min_value, max=max_value, avg=avg_value)
                params.setdefault(dimension_attr, {})[measure_attr] = metric

        dashboard = DashboardT(**params)
        return dashboard
