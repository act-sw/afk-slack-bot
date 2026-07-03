SUPPORTED_LOCALES = ("ru", "en", "pl", "uk")

LANGUAGE_NAMES = {
    "ru": "русский",
    "en": "English",
    "pl": "polski",
    "uk": "українська",
}

_STRINGS = {
    "ru": {
        "afk_confirmation": "Отмечено: отошёл ({duration}).",
        "afk_no_duration": "без указания времени",
        "back_confirmation": "С возвращением!",
        "back_not_afk": "Ты и не отмечался как отошедший.",
        "overdue_dm_text": "⏰ Ты должен был вернуться в {time}. Отметить возвращение?",
        "overdue_button_label": "Вернулся",
        "overdue_dm_resolved": "С возвращением! Отмечено автоматически по кнопке.",
        "lang_set": "Язык бота установлен: {name}.",
        "lang_current": "Текущий язык бота: {name}. Доступно: {options}.",
        "lang_invalid": "Неизвестный язык: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Хорошо, дам знать, когда вернутся: {mentions}.",
        "wait_no_mentions": "Отметь хотя бы одного пользователя: /afk wait @имя",
        "wait_notification": "{name} вернулся(-ась).",
    },
    "en": {
        "afk_confirmation": "Marked as away ({duration}).",
        "afk_no_duration": "no return time given",
        "back_confirmation": "Welcome back!",
        "back_not_afk": "You weren't marked as away.",
        "overdue_dm_text": "⏰ You were expected back at {time}. Mark yourself back?",
        "overdue_button_label": "I'm back",
        "overdue_dm_resolved": "Welcome back! Marked automatically via the button.",
        "lang_set": "Bot language set to: {name}.",
        "lang_current": "Current bot language: {name}. Available: {options}.",
        "lang_invalid": "Unknown language: {input!r}. Available: {options}.",
        "wait_confirmation": "Okay, I'll let you know when back: {mentions}.",
        "wait_no_mentions": "Mention at least one user: /afk wait @name",
        "wait_notification": "{name} is back.",
    },
    "pl": {
        "afk_confirmation": "Odnotowano: nieobecny ({duration}).",
        "afk_no_duration": "bez podanego czasu",
        "back_confirmation": "Witaj z powrotem!",
        "back_not_afk": "Nie byłeś oznaczony jako nieobecny.",
        "overdue_dm_text": "⏰ Miałeś wrócić o {time}. Oznaczyć powrót?",
        "overdue_button_label": "Wróciłem",
        "overdue_dm_resolved": "Witaj z powrotem! Oznaczono automatycznie przyciskiem.",
        "lang_set": "Ustawiono język bota: {name}.",
        "lang_current": "Obecny język bota: {name}. Dostępne: {options}.",
        "lang_invalid": "Nieznany język: {input!r}. Dostępne: {options}.",
        "wait_confirmation": "Dobrze, dam znać, gdy wrócą: {mentions}.",
        "wait_no_mentions": "Oznacz co najmniej jedną osobę: /afk wait @imię",
        "wait_notification": "{name} wrócił(a).",
    },
    "uk": {
        "afk_confirmation": "Відмічено: відійшов ({duration}).",
        "afk_no_duration": "без вказання часу",
        "back_confirmation": "З поверненням!",
        "back_not_afk": "Ти й не відмічався як відсутній.",
        "overdue_dm_text": "⏰ Ти мав повернутися о {time}. Відмітити повернення?",
        "overdue_button_label": "Повернувся",
        "overdue_dm_resolved": "З поверненням! Відмічено автоматично кнопкою.",
        "lang_set": "Мову бота встановлено: {name}.",
        "lang_current": "Поточна мова бота: {name}. Доступно: {options}.",
        "lang_invalid": "Невідома мова: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Добре, дам знати, коли повернуться: {mentions}.",
        "wait_no_mentions": "Познач хоча б одного користувача: /afk wait @ім'я",
        "wait_notification": "{name} повернувся(-лася).",
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
