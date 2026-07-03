import json
import os
from pathlib import Path


class WatchersStore:
    """JSON-file-backed map of target_user_id -> [watcher_user_id, ...].

    A watcher registered via "/afk wait @user" gets DMed once when that
    user's AFK is marked returned, then is removed (one-shot, like the
    overdue reminder's `notified` flag).
    """

    def __init__(self, path: str):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._watchers: dict[str, list[str]] = self._load()

    def _load(self) -> dict[str, list[str]]:
        if not self._path.exists():
            return {}
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self._watchers, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._path)

    def add(self, target_user_id: str, watcher_user_id: str) -> None:
        watchers = self._watchers.setdefault(target_user_id, [])
        if watcher_user_id not in watchers:
            watchers.append(watcher_user_id)
            self._save()

    def list(self, target_user_id: str) -> list[str]:
        """Non-destructive read, for notifications that don't end the watch (e.g. an extension)."""
        return list(self._watchers.get(target_user_id, []))

    def pop_all(self, target_user_id: str) -> list[str]:
        watchers = self._watchers.pop(target_user_id, [])
        if watchers:
            self._save()
        return watchers

    def clear(self) -> None:
        self._watchers = {}
        self._save()
