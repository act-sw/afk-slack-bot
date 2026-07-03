def format_delta(seconds: float) -> str:
    """Render a duration as "14m" (under an hour) or "1:35" (hours:minutes)."""
    total_minutes = round(abs(seconds) / 60)
    if total_minutes < 60:
        return f"{total_minutes}m"
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"
