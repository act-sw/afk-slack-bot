import re
from datetime import datetime, timedelta

_DURATION_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*(h|hour|hours|m|min|minutes)$", re.IGNORECASE)
_UNTIL_RE = re.compile(r"^until\s+(\d{1,2}):(\d{2})$", re.IGNORECASE)


class ParseError(ValueError):
    def __init__(self, text: str):
        self.text = text
        super().__init__(f"could not parse duration: {text!r}")


def parse_expected_return(text: str, now: datetime) -> datetime | None:
    """Parse a duration/time expression into an absolute expected-return datetime.

    Supported: "1.5h", "90m", "until 15:00". Returns None for open-ended AFK
    (e.g. an empty string), meaning no expected return time.
    """
    text = text.strip()
    if not text:
        return None

    match = _DURATION_RE.match(text)
    if match:
        amount = float(match.group(1))
        unit = match.group(2).lower()
        minutes = amount * 60 if unit.startswith("h") else amount
        return now + timedelta(minutes=minutes)

    match = _UNTIL_RE.match(text)
    if match:
        hour, minute = int(match.group(1)), int(match.group(2))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate

    raise ParseError(text)
