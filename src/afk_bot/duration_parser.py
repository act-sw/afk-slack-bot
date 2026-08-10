import math
import re
from datetime import datetime, timedelta

_UNTIL_RE = re.compile(
    r"^until\s+(?:(\d{2})(\d{2})|(\d{1,2}):(\d{2})|(\d{1,2}))\s*(am|pm)?",
    re.IGNORECASE,
)
# A bare "H:MM" (with colon) is unambiguously a clock time even without the
# "until" keyword — a plain duration number never contains a colon.
_BARE_CLOCK_RE = re.compile(r"^(\d{1,2}):(\d{2})\s*(am|pm)?", re.IGNORECASE)
_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
_UNIT_WORD_RE = re.compile(r"^\s*([A-Za-zА-Яа-яЁёІіЇїЄєҐґ]+)")

_HOURS_MAX = 12

# An explicit unit overrides the <=12h/>12m magnitude guess entirely — e.g.
# "13h" is 13 hours (would otherwise misread as 13 minutes), and "5m" is
# 5 minutes (would otherwise misread as 5 hours). Ukrainian "год" is short
# for "година" (hour) — not "год" the Russian word for "year".
_HOUR_UNITS = {
    "h", "hr", "hrs", "hour", "hours",
    "ч", "час", "часа", "часов",
    "год", "година", "години", "годину", "годин",
    "гадзіна", "гадзіны", "гадзін", "гадзіну",
    "godz", "godzina", "godziny", "godzin", "godzinę",
    "hora", "horas",
}
_MINUTE_UNITS = {
    "m", "min", "mins", "minute", "minutes",
    "мин", "минута", "минуты", "минут", "минуту",
    "хв", "хвилина", "хвилини", "хвилин", "хвилину",
    "хвіліна", "хвіліны", "хвілін", "хвіліну",
    "minut", "minuta", "minuty", "minutę",
    "minuto", "minutos",
}


def _resolve_until(now: datetime, hour: int, minute: int, suffix: str | None) -> datetime | None:
    """Resolve an "until" hour/minute (in `now`'s own timezone) to an absolute datetime.

    - With an am/pm suffix, that fixes the 12-hour value unambiguously.
    - Without a suffix and hour in 1-12, it's ambiguous — pick whichever of
      the two 12-hour readings (am/pm) is soonest in the future.
    - Hour 0 or 13-23 is already unambiguous 24-hour notation.
    """
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None

    if suffix:
        hour24 = (hour % 12) + (12 if suffix.lower() == "pm" else 0)
        candidate = now.replace(hour=hour24, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate

    if 1 <= hour <= 12:
        candidates = []
        for hour24 in (hour % 12, (hour % 12) + 12):
            candidate = now.replace(hour=hour24, minute=minute, second=0, microsecond=0)
            if candidate <= now:
                candidate += timedelta(days=1)
            candidates.append(candidate)
        return min(candidates)

    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate


def parse_afk_text(text: str, now: datetime) -> tuple[datetime | None, str]:
    """Split free-form `/afk` text into an expected-return time and a comment.

    `now` must be timezone-aware in the calling user's own timezone — "until"
    times are resolved against it directly.

    - "until" accepts "14", "1400", "14:00", or 12-hour "2pm"/"2:00am".
      Without an am/pm suffix, an hour in 1-12 is ambiguous: it resolves to
      whichever of the two 12-hour readings is soonest (e.g. "until 2" is
      14:00 today if that hasn't passed yet, else 02:00 the next occurrence).
      A bare "H:MM" (e.g. "23:55", "2:30pm") is recognized as a clock time
      the same way even without the "until" keyword, since a plain duration
      number never contains a colon.
    - Otherwise, the first number in the text is the duration. An explicit
      unit right after it (attached or space-separated — "h"/"hr"/"час"/
      "година"/"год"/... for hours, "m"/"min"/"мин"/"хв"/... for minutes)
      overrides the default guess; without one, <=12 is hours and >12 is
      minutes. Minute-valued results round up to a whole minute (comma or
      dot as decimal separator). Everything after the number (and the unit,
      if one was recognized) is the comment.
    - No number at all means an open-ended AFK (no expected return time) and
      the whole text becomes the comment.
    """
    text = text.strip()
    if not text:
        return None, ""

    until_match = _UNTIL_RE.match(text)
    if until_match:
        hhmm_h, hhmm_m, hm_h, hm_m, h_only, suffix = until_match.groups()
        if hhmm_h is not None:
            hour, minute = int(hhmm_h), int(hhmm_m)
        elif hm_h is not None:
            hour, minute = int(hm_h), int(hm_m)
        else:
            hour, minute = int(h_only), 0

        resolved = _resolve_until(now, hour, minute, suffix)
        if resolved is not None:
            return resolved, text[until_match.end() :].strip()

    bare_clock_match = _BARE_CLOCK_RE.match(text)
    if bare_clock_match:
        hour, minute, suffix = bare_clock_match.groups()
        resolved = _resolve_until(now, int(hour), int(minute), suffix)
        if resolved is not None:
            return resolved, text[bare_clock_match.end() :].strip()

    number_match = _NUMBER_RE.search(text)
    if not number_match:
        return None, text

    value = float(number_match.group().replace(",", "."))
    rest = text[number_match.end() :]

    unit_end = 0
    unit_match = _UNIT_WORD_RE.match(rest)
    unit_kind = None
    if unit_match:
        word = unit_match.group(1).lower()
        if word in _HOUR_UNITS:
            unit_kind = "hour"
            unit_end = unit_match.end()
        elif word in _MINUTE_UNITS:
            unit_kind = "minute"
            unit_end = unit_match.end()

    if unit_kind == "hour":
        minutes = value * 60
    elif unit_kind == "minute":
        minutes = math.ceil(value)
    else:
        minutes = value * 60 if value <= _HOURS_MAX else math.ceil(value)

    comment = rest[unit_end:].strip()
    return now + timedelta(minutes=minutes), comment
