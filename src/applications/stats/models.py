from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import NamedTuple
from typing import Optional

from pandas import DataFrame

from project.models import Model


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


@dataclass
class Visit(Model):
    at: Optional[datetime] = None
    cl: Optional[int] = None
    code: Optional[int] = None
    method: Optional[str] = None
    tm: Optional[float] = None
    url: Optional[str] = None

    __json_file__ = "stats.json"

    @classmethod
    def generate_dashboard(cls) -> Optional[DashboardT]:
        df = DataFrame(Visit.all())
        if "at" not in df:
            return None

        try:
            del df["pk"]
        except KeyError:
            pass

        ts_now = datetime.now()
        params = {}

        for measure_attr, minutes in zip(HourlyT.__annotations__, (5, 15, 60, 60 * 24)):
            delta = timedelta(minutes=minutes)
            ts = ts_now - delta

            for dimension_attr, dimension in {"latency": "tm", "traffic": "cl"}.items():
                max_value = df.where(df["at"] >= ts).max()[dimension]
                min_value = df.where(df["at"] >= ts).min()[dimension]
                avg_value = df.where(df["at"] >= ts).mean()[dimension]

                metric = MinMaxT(min=min_value, max=max_value, avg=avg_value)
                params.setdefault(dimension_attr, {})[measure_attr] = metric

        dashboard = DashboardT(**params)
        return dashboard
