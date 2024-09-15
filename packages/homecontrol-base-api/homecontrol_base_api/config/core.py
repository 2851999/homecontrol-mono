import json
from pathlib import Path
from typing import Optional, Type, TypeVar
from pydantic.dataclasses import dataclass


def _get_search_paths(local_file_path: Path) -> list[Path]:
    """Returns a list of paths to search for config (in order they would
    be used)

    First attempts to look in the current directory, then if it doesn't
    exist looks in /etc/homecontrol on Linux, or the home directory on
    Windows/Mac

    :param local_file_path: Local file path as a Path instance
    :return: List of Path's to look for the file at in the order they should be used
    """
    return [
        # Local
        Path.cwd() / local_file_path,
        # Linux
        Path("/etc/homecontrol") / local_file_path,
        # Windows
        Path.home() / local_file_path,
    ]


def _locate_config_file(local_file_path: Path) -> Optional[Path]:
    """Attempts to find the filepath of the config file having searched in the order
    of _get_search_paths"""

    search_paths = _get_search_paths(local_file_path)
    for search_path in search_paths:
        if search_path.exists():
            return search_path
    raise FileNotFoundError(f"Cannot locate the config file '{local_file_path}'")


TDataclass = TypeVar("TDataclass", bound=dataclass)


def load_config(local_file_path: str, dataclass_type: Type[TDataclass]) -> TDataclass:
    """Loads the config from a json file"""
    file_path = _locate_config_file(Path(local_file_path))
    with open(file_path, "r", encoding="utf-8") as file:
        return dataclass_type(**json.load(file))
