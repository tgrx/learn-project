from typing import NamedTuple


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
