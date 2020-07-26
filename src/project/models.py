import json
import os
from dataclasses import asdict
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Tuple
from typing import Union

from django.conf import settings


class ModelError(Exception):
    pass


@dataclass
class Model:
    pk: Optional[str] = None

    __json_file__ = None
    __storage__: Path = (settings.REPO_DIR / "storage").resolve()

    @classmethod
    def all(cls) -> Tuple["Model"]:
        return tuple(cls._build_objects())

    @classmethod
    def one(cls, object_id) -> Union["Model", None]:
        try:
            obj = next(cls._build_objects(lambda record: record[0] == object_id))
        except StopIteration:
            obj = None

        return obj

    def save(self) -> None:
        content = self._load()

        self._setup_pk()
        dct = asdict(self)
        self._shadow_pk(dct)
        content[self.pk] = dct

        self._store(content)

    def delete(self) -> None:
        content = self._load()

        if self.pk not in content:
            return

        del content[self.pk]
        self._store(content)

        self.pk = None

    @classmethod
    def source(cls) -> Path:
        if not cls.__json_file__:
            raise TypeError(f"unbound source for {cls}")
        src = (cls.__storage__ / cls.__json_file__).resolve()
        return src

    def _setup_pk(self):
        if self.pk:
            return

        self.pk = os.urandom(16).hex()

    @staticmethod
    def _shadow_pk(dct: Dict) -> None:
        try:
            del dct["pk"]
        except KeyError:
            pass

    @classmethod
    def _build_objects(
        cls, predicate: Callable = lambda _x: 1
    ) -> Generator["Model", None, None]:
        content = cls._load()

        result = (cls(**kw) for kw in cls._build_kws(content, predicate))

        yield from result

    @classmethod
    def _build_kws(
        cls, content: Dict, predicate: Callable = lambda _x: 1
    ) -> Generator[Dict, None, None]:
        for object_id, fields in filter(predicate, content.items()):
            kw = {}
            for field, field_params in cls.__dataclass_fields__.items():
                value = fields.get(field)
                value = cls._build_value(value, field_params.type)
                kw[field] = value
            kw["pk"] = object_id
            yield kw

    @classmethod
    def _load(cls) -> Dict:
        try:
            with cls.source().open("r") as src:
                payload = src.read()
                if not payload:
                    content = {}
                else:
                    content = json.loads(payload)

        except json.JSONDecodeError as err:
            raise ModelError("corrupted source") from err

        except FileNotFoundError:
            content = {}

        return content

    @classmethod
    def _store(cls, content: Dict) -> None:
        cleaned_content = cls._clean_content(content)
        with cls.source().open("w") as dst:
            json.dump(cleaned_content, dst)

    @classmethod
    def _validate_fields(cls, kwargs: Dict):
        updated_set = set(kwargs)
        allowed_set = set(cls.__dataclass_fields__)
        diff = updated_set - allowed_set
        if diff:
            raise ValueError(f"fields {sorted(diff)} are not supported by {cls}")

    @classmethod
    def _clean_content(cls, content: Dict) -> Dict:
        result = {}

        for key, value in content.items():
            if isinstance(value, (date, datetime)):
                value = value.strftime("%Y-%m-%d")
            elif isinstance(value, dict):
                value = cls._clean_content(value)
            result[key] = value

        return result

    @classmethod
    def _build_value(cls, value, field_type):
        if issubclass(date, field_type.__args__):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value
