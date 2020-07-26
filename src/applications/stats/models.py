from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from project.models import Model


@dataclass
class Visit(Model):
    at: Optional[datetime] = None
    code: Optional[int] = None
    method: Optional[str] = None
    tm: Optional[float] = None
    url: Optional[str] = None

    __json_file__ = "stats.json"
