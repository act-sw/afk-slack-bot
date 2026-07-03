import math
import re
from datetime import datetime, timedelta

_UNTIL_RE = re.compile(r"^until\s+(\d{1,2}):(\d{2})", re.IGNORECASE)
_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")

_HOURS_MAX = 12


def parse_afk_text(text: str, now: datetime) -> tuple[datetime | None, str]:
    """Split free-form `/afk` text into an expected-return time and a comment.

    - "until HH:MM ..." sets an absolute return time.
    - Otherwise, the first number in the text is the duration: <=12 is hours,
      >12 is minutes (comma or dot as decimal separator). Everything after
      that number is the comment.
    - No number at all means an open-ended AFK (no expected return time) and
      the whole text becomes the comment.
    """
    text = text.strip()
    if not text:
        return None, ""

    until_match = _UNTIL_RE.match(text)
    if until_match:
        hour, minute = int(until_match.group(1)), int(until_match.group(2))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate, text[until_match.end() :].strip()

    number_match = _NUMBER_RE.search(text)
    if not number_match:
        return None, text

    value = float(number_match.group().replace(",", "."))
    minutes = value * 60 if value <= _HOURS_MAX else math.ceil(value)
    comment = text[number_match.end() :].strip()
    return now + timedelta(minutes=minutes), comment
