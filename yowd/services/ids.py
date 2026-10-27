"""Sequential identifier generator (e.g. YD-0001) backed by the store."""
from yowd.storage.json_store import JsonStore

_COUNTERS = "counters"


class IdGenerator:
    """Issue unique, human-readable IDs that survive restarts."""

    def __init__(self, store: JsonStore) -> None:
        """Bind the generator to a persistence store."""
        self._store = store

    def next_id(self, prefix: str) -> str:
        """Return the next ID for ``prefix``, e.g. ``YD-0001``."""
        counters = self._store.load_dict(_COUNTERS)
        number = int(counters.get(prefix, 0)) + 1
        counters[prefix] = number
        self._store.save(_COUNTERS, counters)
        return f"{prefix}-{number:04d}"
