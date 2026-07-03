import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class AfkEntry:
    user_id: str
    name: str
    start_ts: float
    expected_return_ts: float | None
    comment: str


class StateStore:
    """JSON-file-backed store of current AFK entries.

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
        return {uid: AfkEntry(**entry) for uid, entry in raw.items()}

    def _save(self) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump({uid: asdict(e) for uid, e in self._entries.items()}, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._path)

    def upsert(self, entry: AfkEntry) -> None:
        self._entries[entry.user_id] = entry
        self._save()

    def remove(self, user_id: str) -> bool:
        if user_id not in self._entries:
            return False
        del self._entries[user_id]
        self._save()
        return True

    def clear(self) -> None:
        self._entries = {}
        self._save()

    def all(self) -> list[AfkEntry]:
        return list(self._entries.values())
