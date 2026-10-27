"""Simple JSON file persistence (one file per collection)."""
import json
from pathlib import Path
from typing import Any

from yowd.constants import DATA_DIR


class JsonStore:
    """Load and save named collections as ``<data_dir>/<name>.json``."""

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        """Create the data directory if it does not exist."""
        self._dir = data_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self._dir / f"{name}.json"

    def load_list(self, name: str) -> list[dict[str, Any]]:
        """Return a stored list of records (empty if none saved yet)."""
        data = self._read(name, [])
        return data if isinstance(data, list) else []

    def load_dict(self, name: str) -> dict[str, Any]:
        """Return a stored dictionary (empty if none saved yet)."""
        data = self._read(name, {})
        return data if isinstance(data, dict) else {}

    def save(self, name: str, data: list[Any] | dict[str, Any]) -> None:
        """Write data atomically so a crash cannot corrupt the file."""
        tmp = self._path(name).with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(self._path(name))

    def _read(self, name: str, default: Any) -> Any:
        path = self._path(name)
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default
