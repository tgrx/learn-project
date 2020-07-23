import json
from pathlib import Path
from typing import Dict
from typing import Union
from urllib.parse import parse_qs

from django.conf import settings
from django.http import Http404
from django.http import HttpRequest

from project.consts import BINARY_EXTENSIONS
from project.consts import USER_SESSIONS


def load_user_session(request: HttpRequest) -> Dict:
    session = request.session
    if not session or session.is_empty():
        return {}
    return session


def get_session_id(request: HttpRequest) -> Union[str, None]:
    cookie = request.headers.get("Cookie")
    if not cookie:
        return None

    qs, *_extra = cookie.split(";")
    args = linearize_qs(parse_qs(qs))
    session_id = args.get("SID")
    return session_id


def linearize_qs(qs: Dict) -> Dict:
    """
    Linearizes qs dict: only the first value is populated into result
    """
    result = {}

    for key, values in qs.items():
        if not values:
            continue

        value = values
        if isinstance(values, list):
            value = values[0]

        result[key] = value

    return result


def load_sessions_file() -> Dict:
    try:
        with USER_SESSIONS.open("r") as fp:
            return json.load(fp)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def build_query_args(request: HttpRequest) -> Dict:
    qs = request.GET
    if not qs:
        return {}

    args = linearize_qs(qs)

    return args


def build_name(query_args: Dict) -> str:
    return query_args.get("name", "Anonymous")


def build_age(query_args: Dict) -> Union[int, None]:
    age = query_args.get("age")
    if age is None:
        return age
    return int(age)


def get_static_content(file_path: Union[str, Path]) -> Union[str, bytes]:
    """
    Returns the content of the file given by path
    Guesses the type of file and returns str/bytes respectively
    """

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.is_file():
        raise Http404

    binary_flag = "b" if file_path.suffix.lower() in BINARY_EXTENSIONS else ""

    with file_path.open(f"r{binary_flag}") as src:
        ct = src.read()

    return ct


def _count_visits(path):
    stats_file: Path = settings.REPO_DIR / "stats.json"
    stats = {}

    if stats_file.is_file():
        try:
            with stats_file.open("r") as fp:
                stats = json.load(fp)
        except json.JSONDecodeError:
            pass

    if path not in stats:
        stats[path] = 0

    stats[path] += 1

    with stats_file.open("w") as fp:
        json.dump(stats, fp)


def count_visits(view):
    def _view(request: HttpRequest, *a, **k):
        try:
            resp = view(request, *a, **k)
            return resp
        finally:
            _count_visits(request.path)

    return _view
