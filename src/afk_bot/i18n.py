SUPPORTED_LOCALES = ("ru", "en")

_STRINGS = {
    "ru": {
        "afk_confirmation": "Отмечено: отошёл ({duration}).",
        "afk_no_duration": "без указания времени",
        "parse_error": "Не удалось распознать длительность: {text!r}",
        "back_confirmation": "С возвращением!",
        "back_not_afk": "Ты и не отмечался как отошедший.",
        "overdue_dm_text": "⏰ Ты должен был вернуться в {time}. Отметить возвращение?",
        "overdue_button_label": "Вернулся",
        "overdue_dm_resolved": "С возвращением! Отмечено автоматически по кнопке.",
        "canvas_empty": "_Сейчас все на месте._",
        "canvas_headers": ["Имя", "Ушёл в", "Вернётся ~", "Комментарий"],
        "canvas_overdue_marker": "⏰ задержался",
    },
    "en": {
        "afk_confirmation": "Marked as away ({duration}).",
        "afk_no_duration": "no return time given",
        "parse_error": "Could not parse duration: {text!r}",
        "back_confirmation": "Welcome back!",
        "back_not_afk": "You weren't marked as away.",
        "overdue_dm_text": "⏰ You were expected back at {time}. Mark yourself back?",
        "overdue_button_label": "I'm back",
        "overdue_dm_resolved": "Welcome back! Marked automatically via the button.",
        "canvas_empty": "_Everyone's around._",
        "canvas_headers": ["Name", "Left at", "Returns ~", "Comment"],
        "canvas_overdue_marker": "⏰ overdue",
    },
}


def resolve_locale(raw_locale: str | None, default: str) -> str:
    if not raw_locale:
        return default
    candidate = raw_locale.split("-")[0].lower()
    return candidate if candidate in SUPPORTED_LOCALES else default


def t(locale: str, key: str, **kwargs) -> str:
    strings = _STRINGS.get(locale, _STRINGS["ru"])
    value = strings[key]
    return value.format(**kwargs) if isinstance(value, str) else value
