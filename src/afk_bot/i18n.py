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
        "overdue_dm_text": "⏰ Доступность запланирована с {time}",
        "overdue_button_label": "Я уже здесь",
        "extend_button_label": "Мне нужно ещё полчаса",
        "extend_confirmation": "Хорошо, +30 минут (новая оценка: {time}).",
        "lang_set": "Язык бота установлен: {name}.",
        "lang_current": "Текущий язык бота: {name}. Доступно: {options}.",
        "lang_invalid": "Неизвестный язык: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Дам знать, когда они вернутся: {mentions}.",
        "wait_no_mentions": "Отметь хотя бы одного пользователя: /afk wait @имя",
        "wait_notification": "{name} вернулся(-ась).",
        "wait_extended_notification": "{name} нужно ещё полчаса.",
        "wait_target_notification": "{name} ждёт твоего возвращения — если получится, свяжись с ним(-ней) заранее.",
        "help_text": (
            "*Команды:*\n"
            "• `/afk N [комментарий]` — отметить, что отошёл (N ≤12 — часы, >12 — минуты)\n"
            "• `/afk back` — отметить возвращение\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — язык бота (без аргумента — показать текущий)\n"
            "• `/afk wait @user [@user2 ...]` — узнать, когда вернутся указанные люди\n"
            "• `/afk help` — эта подсказка"
        ),
    },
    "en": {
        "afk_confirmation_duration": "See you in {duration}!",
        "afk_confirmation_open": "Marked as away.",
        "back_confirmation_with_delta": "Welcome back! You made it in {duration} ({delta}).",
        "back_confirmation_no_delta": "Welcome back! You were away for {duration}.",
        "back_not_afk": "You weren't marked as away.",
        "delta_less": "{amount} less",
        "delta_more": "{amount} more",
        "overdue_dm_text": "⏰ Expected availability from {time}",
        "overdue_button_label": "I'm here",
        "extend_button_label": "I need 30 more minutes",
        "extend_confirmation": "Okay, +30 minutes (new estimate: {time}).",
        "lang_set": "Bot language set to: {name}.",
        "lang_current": "Current bot language: {name}. Available: {options}.",
        "lang_invalid": "Unknown language: {input!r}. Available: {options}.",
        "wait_confirmation": "I'll let you know when they are back: {mentions}.",
        "wait_no_mentions": "Mention at least one user: /afk wait @name",
        "wait_notification": "{name} is back.",
        "wait_extended_notification": "{name} needs 30 more minutes.",
        "wait_target_notification": "{name} is waiting for you to be back — reach out to them first if you can.",
        "help_text": (
            "*Commands:*\n"
            "• `/afk N [comment]` — mark yourself away (N ≤12 = hours, >12 = minutes)\n"
            "• `/afk back` — mark your return\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — bot language (no argument shows current)\n"
            "• `/afk wait @user [@user2 ...]` — get notified when the mentioned people are back\n"
            "• `/afk help` — this message"
        ),
    },
    "pl": {
        "afk_confirmation_duration": "Do zobaczenia za {duration}!",
        "afk_confirmation_open": "Odnotowano: nieobecny.",
        "back_confirmation_with_delta": "Witaj z powrotem! Zrobiłeś to w {duration} ({delta}).",
        "back_confirmation_no_delta": "Witaj z powrotem! Byłeś nieobecny {duration}.",
        "back_not_afk": "Nie byłeś oznaczony jako nieobecny.",
        "delta_less": "o {amount} mniej",
        "delta_more": "o {amount} więcej",
        "overdue_dm_text": "⏰ Dostępność zaplanowana od {time}",
        "overdue_button_label": "Już tu jestem",
        "extend_button_label": "Potrzebuję jeszcze 30 minut",
        "extend_confirmation": "Dobrze, +30 minut (nowy szacunek: {time}).",
        "lang_set": "Ustawiono język bota: {name}.",
        "lang_current": "Obecny język bota: {name}. Dostępne: {options}.",
        "lang_invalid": "Nieznany język: {input!r}. Dostępne: {options}.",
        "wait_confirmation": "Dam znać, gdy wrócą: {mentions}.",
        "wait_no_mentions": "Oznacz co najmniej jedną osobę: /afk wait @imię",
        "wait_notification": "{name} wrócił(a).",
        "wait_extended_notification": "{name} potrzebuje jeszcze 30 minut.",
        "wait_target_notification": "{name} czeka na Twój powrót — skontaktuj się z nim/nią najpierw, jeśli możesz.",
        "help_text": (
            "*Polecenia:*\n"
            "• `/afk N [komentarz]` — oznacz nieobecność (N ≤12 = godziny, >12 = minuty)\n"
            "• `/afk back` — oznacz powrót\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — język bota (bez argumentu pokazuje obecny)\n"
            "• `/afk wait @user [@user2 ...]` — dowiedz się, kiedy wskazane osoby wrócą\n"
            "• `/afk help` — ta wiadomość"
        ),
    },
    "uk": {
        "afk_confirmation_duration": "Побачимось через {duration}!",
        "afk_confirmation_open": "Відмічено: відійшов.",
        "back_confirmation_with_delta": "З поверненням! Ти впорався за {duration} ({delta}).",
        "back_confirmation_no_delta": "З поверненням! Ти був відсутній {duration}.",
        "back_not_afk": "Ти й не відмічався як відсутній.",
        "delta_less": "на {amount} менше",
        "delta_more": "на {amount} більше",
        "overdue_dm_text": "⏰ Доступність запланована з {time}",
        "overdue_button_label": "Я вже тут",
        "extend_button_label": "Мені потрібно ще 30 хвилин",
        "extend_confirmation": "Гаразд, +30 хвилин (нова оцінка: {time}).",
        "lang_set": "Мову бота встановлено: {name}.",
        "lang_current": "Поточна мова бота: {name}. Доступно: {options}.",
        "lang_invalid": "Невідома мова: {input!r}. Доступно: {options}.",
        "wait_confirmation": "Дам знати, коли вони повернуться: {mentions}.",
        "wait_no_mentions": "Познач хоча б одного користувача: /afk wait @ім'я",
        "wait_notification": "{name} повернувся(-лася).",
        "wait_extended_notification": "{name} потрібно ще 30 хвилин.",
        "wait_target_notification": "{name} чекає на твоє повернення — якщо вийде, звʼяжись із ним(-нею) спершу.",
        "help_text": (
            "*Команди:*\n"
            "• `/afk N [коментар]` — відмітити, що відійшов (N ≤12 — години, >12 — хвилини)\n"
            "• `/afk back` — відмітити повернення\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — мова бота (без аргументу — показати поточну)\n"
            "• `/afk wait @user [@user2 ...]` — дізнатись, коли повернуться вказані люди\n"
            "• `/afk help` — ця підказка"
        ),
    },
    "be": {
        "afk_confirmation_duration": "Пабачымся праз {duration}!",
        "afk_confirmation_open": "Адзначана: адышоў.",
        "back_confirmation_with_delta": "З вяртаннем! Ты справіўся за {duration} ({delta}).",
        "back_confirmation_no_delta": "З вяртаннем! Цябе не было {duration}.",
        "back_not_afk": "Ты і не адзначаўся як адсутны.",
        "delta_less": "на {amount} менш",
        "delta_more": "на {amount} больш",
        "overdue_dm_text": "⏰ Даступнасць запланавана з {time}",
        "overdue_button_label": "Я ужо тут",
        "extend_button_label": "Мне трэба яшчэ 30 хвілін",
        "extend_confirmation": "Добра, +30 хвілін (новая ацэнка: {time}).",
        "lang_set": "Мову бота ўстаноўлена: {name}.",
        "lang_current": "Бягучая мова бота: {name}. Даступна: {options}.",
        "lang_invalid": "Невядомая мова: {input!r}. Даступна: {options}.",
        "wait_confirmation": "Дам ведаць, калі яны вернуцца: {mentions}.",
        "wait_no_mentions": "Пазнач хаця б аднаго карыстальніка: /afk wait @імя",
        "wait_notification": "{name} вярнуўся(-лася).",
        "wait_extended_notification": "{name} трэба яшчэ 30 хвілін.",
        "wait_target_notification": "{name} чакае твайго вяртання — калі атрымаецца, звяжыся з ім(-ёй) спачатку.",
        "help_text": (
            "*Каманды:*\n"
            "• `/afk N [каментар]` — адзначыць, што адышоў (N ≤12 — гадзіны, >12 — хвіліны)\n"
            "• `/afk back` — адзначыць вяртанне\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — мова бота (без аргумента — паказаць бягучую)\n"
            "• `/afk wait @user [@user2 ...]` — даведацца, калі вернуцца ўказаныя людзі\n"
            "• `/afk help` — гэтая падказка"
        ),
    },
    "es": {
        "afk_confirmation_duration": "¡Nos vemos en {duration}!",
        "afk_confirmation_open": "Marcado como ausente.",
        "back_confirmation_with_delta": "¡Bienvenido de vuelta! Lo lograste en {duration} ({delta}).",
        "back_confirmation_no_delta": "¡Bienvenido de vuelta! Estuviste ausente {duration}.",
        "back_not_afk": "No estabas marcado como ausente.",
        "delta_less": "{amount} menos",
        "delta_more": "{amount} más",
        "overdue_dm_text": "⏰ Disponibilidad prevista desde las {time}",
        "overdue_button_label": "Ya estoy aquí",
        "extend_button_label": "Necesito 30 minutos más",
        "extend_confirmation": "Vale, +30 minutos (nueva estimación: {time}).",
        "lang_set": "Idioma del bot configurado en: {name}.",
        "lang_current": "Idioma actual del bot: {name}. Disponibles: {options}.",
        "lang_invalid": "Idioma desconocido: {input!r}. Disponibles: {options}.",
        "wait_confirmation": "Te avisaré cuando vuelvan: {mentions}.",
        "wait_no_mentions": "Menciona al menos un usuario: /afk wait @nombre",
        "wait_notification": "{name} ha vuelto.",
        "wait_extended_notification": "{name} necesita 30 minutos más.",
        "wait_target_notification": "{name} está esperando a que vuelvas — contacta con él/ella primero si puedes.",
        "help_text": (
            "*Comandos:*\n"
            "• `/afk N [comentario]` — márcate como ausente (N ≤12 = horas, >12 = minutos)\n"
            "• `/afk back` — marca tu regreso\n"
            "• `/afk lang [ru|en|pl|uk|be|es]` — idioma del bot (sin argumento muestra el actual)\n"
            "• `/afk wait @user [@user2 ...]` — recibe un aviso cuando vuelvan las personas mencionadas\n"
            "• `/afk help` — este mensaje"
        ),
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
