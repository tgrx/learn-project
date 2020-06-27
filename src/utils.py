from pathlib import Path
from typing import Dict
from typing import Union

from consts import BINARY_EXTENSIONS
from errors import NotFound


def get_static_content(file_path: Union[str, Path]) -> Union[str, bytes]:
    """
    Returns the content of the file given by path
    Guesses the type of file and returns str/bytes respectively
    """

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.is_file():
        raise NotFound(extra=file_path.resolve())

    binary_flag = "b" if file_path.suffix.lower() in BINARY_EXTENSIONS else ""

    with file_path.open(f"r{binary_flag}") as src:
        ct = src.read()

    return ct


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


def h(header: str) -> str:
    return "-".join(part.capitalize() for part in header.split("-"))
