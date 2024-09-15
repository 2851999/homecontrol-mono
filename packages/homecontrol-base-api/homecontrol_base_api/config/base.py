import json
from pathlib import Path
from typing import Generic, Optional, Type, TypeVar
from pydantic.dataclasses import dataclass


TDataclass = TypeVar("TDataclass", bound=dataclass)


class Config(Generic[TDataclass]):

    _data: TDataclass
    _local_file_path: Path
    _dataclass_type: Type[TDataclass]

    def __init__(self, local_file_path: str, dataclass_type: Type[TDataclass]):
        """Load when initialised"""

        self._local_file_path = Path(local_file_path)
        self._dataclass_type = dataclass_type

        self.load()

    def load(self):
        """Loads the config from a json file"""
        file_path = self.get_file_path()
        with open(file_path, "r", encoding="utf-8") as file:
            self._data = self._dataclass_type(**json.load(file))

    def _get_search_paths(self) -> list[Path]:
        """Returns a list of paths to search for config (in order they would
        be used)

        First attempts to look in the current directory, then if it doesn't
        exist looks in /etc/homecontrol on Linux, or the home directory on
        Windows/Mac
        """
        return [
            # Local
            Path.cwd() / self._local_file_path,
            # Linux
            Path("/etc/homecontrol") / self._local_file_path,
            # Windows
            Path.home() / self._local_file_path,
        ]

    def get_file_path(self) -> Optional[Path]:
        """Attempts to find the filepath of the config file having searched in the order
        of _get_search_paths"""

        search_paths = self._get_search_paths()
        for search_path in search_paths:
            if search_path.exists():
                return search_path
        raise FileNotFoundError(
            f"Cannot locate the config file '{self._local_file_path}'"
        )
