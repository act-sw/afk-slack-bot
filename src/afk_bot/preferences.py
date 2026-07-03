import json
import os
from pathlib import Path


class PreferencesStore:
    """JSON-file-backed per-user preferences (currently just bot response language)."""

    def __init__(self, path: str):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._locales: dict[str, str] = self._load()

    def _load(self) -> dict[str, str]:
        if not self._path.exists():
            return {}
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        tmp_path = self._path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self._locales, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._path)

    def get_locale(self, user_id: str) -> str | None:
        return self._locales.get(user_id)

    def set_locale(self, user_id: str, locale: str) -> None:
        self._locales[user_id] = locale
        self._save()
