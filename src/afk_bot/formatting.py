def format_delta(seconds: float) -> str:
    """Render a duration as "14m" (under an hour) or "1:35" (hours:minutes)."""
    total_minutes = round(abs(seconds) / 60)
    if total_minutes < 60:
        return f"{total_minutes}m"
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"


def format_countdown(seconds: float) -> str:
    """Render a signed countdown as "2h15m", "49m", or "− 1h15m".

    Uses a real minus sign (U+2212), not a hyphen, because a leading
    "- " inside a markdown table cell renders as a bullet point in Slack
    Canvas.
    """
    sign = "− " if seconds < 0 else ""
    total_minutes = round(abs(seconds) / 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours:
        return f"{sign}{hours}h{minutes}m"
    return f"{sign}{minutes}m"


_SLAVIC_LOCALES = {"ru", "uk", "be", "pl"}

# Slavic "one" forms are accusative singular (every caller embeds these in an
# accusative-governing phrase: "через X", "за X", or a bare duration
# complement like "отсутствовал X"). "Час"-type words are masculine
# inanimate, so accusative == nominative there; the feminine "minute"/"hour"
# words (minute in all four, hour in uk/be/pl) differ from their nominative
# form ("минута" -> "минуту", "godzina" -> "godzinę", etc). The 2-4/5+ forms
# are genitive singular/plural, which don't change with the governing case.
_UNIT_WORDS = {
    "ru": {"hour": ("час", "часа", "часов"), "minute": ("минуту", "минуты", "минут")},
    "uk": {"hour": ("годину", "години", "годин"), "minute": ("хвилину", "хвилини", "хвилин")},
    "be": {"hour": ("гадзіну", "гадзіны", "гадзін"), "minute": ("хвіліну", "хвіліны", "хвілін")},
    "pl": {"hour": ("godzinę", "godziny", "godzin"), "minute": ("minutę", "minuty", "minut")},
    "en": {"hour": ("hour", "hours", "hours"), "minute": ("minute", "minutes", "minutes")},
    "es": {"hour": ("hora", "horas", "horas"), "minute": ("minuto", "minutos", "minutos")},
}


def _slavic_form(n: int, forms: tuple[str, str, str]) -> str:
    n100 = n % 100
    n10 = n % 10
    if 10 <= n100 <= 20:
        return forms[2]
    if n10 == 1:
        return forms[0]
    if 2 <= n10 <= 4:
        return forms[1]
    return forms[2]


def _unit_word(n: int, unit: str, locale: str) -> str:
    forms = _UNIT_WORDS.get(locale, _UNIT_WORDS["en"])[unit]
    if locale in _SLAVIC_LOCALES:
        return _slavic_form(n, forms)
    return forms[0] if n == 1 else forms[1]


def format_duration_words(seconds: float, locale: str) -> str:
    """Render a duration in full localized words, e.g. "45 minutes", "1 hour 20 minutes"."""
    total_minutes = round(abs(seconds) / 60)
    hours, minutes = divmod(total_minutes, 60)
    parts = []
    if hours:
        parts.append(f"{hours} {_unit_word(hours, 'hour', locale)}")
    if minutes or not hours:
        parts.append(f"{minutes} {_unit_word(minutes, 'minute', locale)}")
    return " ".join(parts)
