from dataclasses import dataclass
from datetime import date
from typing import Optional

from project.models import Model


@dataclass
class Project(Model):
    name: Optional[str] = None
    description: Optional[str] = None
    started: Optional[date] = None
    ended: Optional[date] = None

    __json_file__ = "projects.json"
