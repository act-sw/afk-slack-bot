SUPPORTED_LOCALES = ("ru", "en", "pl", "uk", "be", "es")

LANGUAGE_NAMES = {
    "ru": "русский",
    "en": "English",
    "pl": "polski",
    "uk": "українська",
    "be": "беларуская",
    "es": "español",
}

_STRINGS = {
    "ru": {
        "afk_confirmation_duration": "Увидимся через {duration}!",
        "afk_confirmation_open": "Отмечено: отошёл.",
        "back_confirmation_with_delta": "С возвращением! Вы справились за {duration} ({delta}).",
        "back_confirmation_no_delta": "С возвращением! Вы отсутствовали {duration}.",
        "back_not_afk": "Ты и не отмечался как отошедший.",
        "delta_less": "на {amount} меньше",
        "delta_more": "на {amount} больше",
        "overdue_dm_text": "⏰ Ты должен был вернуться в {time}. Отметить возвращение?",
        "overdue_button_label": "Вернулся",
        "lang_set": "Язык бота установлен: {name}.",
        "lang_current": "Текущий язык бота: {name}. Доступно: {options}.",
        "lang_invalid": "Неизвестный язык: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Дам знать, когда они вернутся: {mentions}.",
        "wait_no_mentions": "Отметь хотя бы одного пользователя: /afk wait @имя",
        "wait_notification": "{name} вернулся(-ась).",
    },
    "en": {
        "afk_confirmation_duration": "See you in {duration}!",
        "afk_confirmation_open": "Marked as away.",
        "back_confirmation_with_delta": "Welcome back! You made it in {duration} ({delta}).",
        "back_confirmation_no_delta": "Welcome back! You were away for {duration}.",
        "back_not_afk": "You weren't marked as away.",
        "delta_less": "{amount} less",
        "delta_more": "{amount} more",
        "overdue_dm_text": "⏰ You were expected back at {time}. Mark yourself back?",
        "overdue_button_label": "I'm back",
        "lang_set": "Bot language set to: {name}.",
        "lang_current": "Current bot language: {name}. Available: {options}.",
        "lang_invalid": "Unknown language: {input!r}. Available: {options}.",
        "wait_confirmation": "I'll let you know when they are back: {mentions}.",
        "wait_no_mentions": "Mention at least one user: /afk wait @name",
        "wait_notification": "{name} is back.",
    },
    "pl": {
        "afk_confirmation_duration": "Do zobaczenia za {duration}!",
        "afk_confirmation_open": "Odnotowano: nieobecny.",
        "back_confirmation_with_delta": "Witaj z powrotem! Zrobiłeś to w {duration} ({delta}).",
        "back_confirmation_no_delta": "Witaj z powrotem! Byłeś nieobecny {duration}.",
        "back_not_afk": "Nie byłeś oznaczony jako nieobecny.",
        "delta_less": "o {amount} mniej",
        "delta_more": "o {amount} więcej",
        "overdue_dm_text": "⏰ Miałeś wrócić o {time}. Oznaczyć powrót?",
        "overdue_button_label": "Wróciłem",
        "lang_set": "Ustawiono język bota: {name}.",
        "lang_current": "Obecny język bota: {name}. Dostępne: {options}.",
        "lang_invalid": "Nieznany język: {input!r}. Dostępne: {options}.",
        "wait_confirmation": "Dam znać, gdy wrócą: {mentions}.",
        "wait_no_mentions": "Oznacz co najmniej jedną osobę: /afk wait @imię",
        "wait_notification": "{name} wrócił(a).",
    },
    "uk": {
        "afk_confirmation_duration": "Побачимось через {duration}!",
        "afk_confirmation_open": "Відмічено: відійшов.",
        "back_confirmation_with_delta": "З поверненням! Ти впорався за {duration} ({delta}).",
        "back_confirmation_no_delta": "З поверненням! Ти був відсутній {duration}.",
        "back_not_afk": "Ти й не відмічався як відсутній.",
        "delta_less": "на {amount} менше",
        "delta_more": "на {amount} більше",
        "overdue_dm_text": "⏰ Ти мав повернутися о {time}. Відмітити повернення?",
        "overdue_button_label": "Повернувся",
        "lang_set": "Мову бота встановлено: {name}.",
        "lang_current": "Поточна мова бота: {name}. Доступно: {options}.",
        "lang_invalid": "Невідома мова: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Дам знати, коли вони повернуться: {mentions}.",
        "wait_no_mentions": "Познач хоча б одного користувача: /afk wait @ім'я",
        "wait_notification": "{name} повернувся(-лася).",
    },
    "be": {
        "afk_confirmation_duration": "Пабачымся праз {duration}!",
        "afk_confirmation_open": "Адзначана: адышоў.",
        "back_confirmation_with_delta": "З вяртаннем! Ты справіўся за {duration} ({delta}).",
        "back_confirmation_no_delta": "З вяртаннем! Цябе не было {duration}.",
        "back_not_afk": "Ты і не адзначаўся як адсутны.",
        "delta_less": "на {amount} менш",
        "delta_more": "на {amount} больш",
        "overdue_dm_text": "⏰ Ты павінен быў вярнуцца ў {time}. Адзначыць вяртанне?",
        "overdue_button_label": "Вярнуўся",
        "lang_set": "Мову бота ўстаноўлена: {name}.",
        "lang_current": "Бягучая мова бота: {name}. Даступна: {options}.",
        "lang_invalid": "Невядомая мова: {input!r}. Даступна: {options}.",
        "wait_confirmation": "Дам ведаць, калі яны вернуцца: {mentions}.",
        "wait_no_mentions": "Пазнач хаця б аднаго карыстальніка: /afk wait @імя",
        "wait_notification": "{name} вярнуўся(-лася).",
    },
    "es": {
        "afk_confirmation_duration": "¡Nos vemos en {duration}!",
        "afk_confirmation_open": "Marcado como ausente.",
        "back_confirmation_with_delta": "¡Bienvenido de vuelta! Lo lograste en {duration} ({delta}).",
        "back_confirmation_no_delta": "¡Bienvenido de vuelta! Estuviste ausente {duration}.",
        "back_not_afk": "No estabas marcado como ausente.",
        "delta_less": "{amount} menos",
        "delta_more": "{amount} más",
        "overdue_dm_text": "⏰ Se esperaba que volvieras a las {time}. ¿Marcar tu regreso?",
        "overdue_button_label": "He vuelto",
        "lang_set": "Idioma del bot configurado en: {name}.",
        "lang_current": "Idioma actual del bot: {name}. Disponibles: {options}.",
        "lang_invalid": "Idioma desconocido: {input!r}. Disponibles: {options}.",
        "wait_confirmation": "Te avisaré cuando vuelvan: {mentions}.",
        "wait_no_mentions": "Menciona al menos un usuario: /afk wait @nombre",
        "wait_notification": "{name} ha vuelto.",
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
