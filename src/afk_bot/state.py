import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class AfkEntry:
    entry_id: str
    user_id: str
    name: str
    start_ts: float
    expected_return_ts: float | None
    comment: str
    tz: str
    locale: str
    notified: bool = False
    returned_ts: float | None = None
    extended: bool = False
    original_expected_return_ts: float | None = None
    time_format: str = "24"


class StateStore:
    """JSON-file-backed store of AFK entries, keyed by entry_id.

    A user can have multiple entries in the same day (e.g. AFK, back, AFK
    again) — only the entry with `returned_ts is None`, if any, is "active".

    Not safe for concurrent writers — callers must serialize access
    (the single queue worker in queue_worker.py does this).
    """

    def __init__(self, path: str):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._entries: dict[str, AfkEntry] = self._load()

    def _load(self) -> dict[str, AfkEntry]:
        if not self._path.exists():
            return {}
        with open(self._path, encoding="utf-8") as f:
            raw = json.load(f)
        return {eid: AfkEntry(**entry) for eid, entry in raw.items()}

    def _save(self) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump({eid: asdict(e) for eid, e in self._entries.items()}, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._path)

    def upsert(self, entry: AfkEntry) -> None:
        self._entries[entry.entry_id] = entry
        self._save()

    def get_active(self, user_id: str) -> AfkEntry | None:
        for entry in self._entries.values():
            if entry.user_id == user_id and entry.returned_ts is None:
                return entry
        return None

    def clear(self) -> None:
        self._entries = {}
        self._save()

    def all(self) -> list[AfkEntry]:
        return list(self._entries.values())
