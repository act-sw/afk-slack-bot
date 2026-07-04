import json
import os
from pathlib import Path


class PreferencesStore:
    """JSON-file-backed per-user preferences: bot response language and time format."""

    def __init__(self, path: str):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._prefs: dict[str, dict] = self._load()

    def _load(self) -> dict[str, dict]:
        if not self._path.exists():
            return {}
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self._prefs, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._path)

    def get_locale(self, user_id: str) -> str | None:
        return self._prefs.get(user_id, {}).get("locale")

    def set_locale(self, user_id: str, locale: str) -> None:
        self._prefs.setdefault(user_id, {})["locale"] = locale
        self._save()

    def get_time_format(self, user_id: str) -> str | None:
        return self._prefs.get(user_id, {}).get("time_format")

    def set_time_format(self, user_id: str, time_format: str) -> None:
        self._prefs.setdefault(user_id, {})["time_format"] = time_format
        self._save()
