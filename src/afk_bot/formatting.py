def format_delta(seconds: float) -> str:
    """Render a duration as "14m" (under an hour) or "1:35" (hours:minutes)."""
    total_minutes = round(abs(seconds) / 60)
    if total_minutes < 60:
        return f"{total_minutes}m"
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"


def format_countdown(seconds: float) -> str:
    """Render a signed countdown as "2h 15m", "49 min", or "- 1h 15m"."""
    sign = "- " if seconds < 0 else ""
    total_minutes = round(abs(seconds) / 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours:
        return f"{sign}{hours}h {minutes}m"
    return f"{sign}{minutes} min"
