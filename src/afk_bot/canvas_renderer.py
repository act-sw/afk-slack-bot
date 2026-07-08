import math
from datetime import datetime
from zoneinfo import ZoneInfo

from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.formatting import format_countdown, format_delta
from afk_bot.state import AfkEntry

_HEADERS_AWAY = ["Name", "Back in", "AFK since", "Estimated return", "Comment"]
_HEADERS_RETURNED = ["Name", "Back in", "AFK since", "Returned at", "Comment"]


def fmt_time(ts: float | None, tz_name: str, time_format: str = "24") -> str:
    if ts is None:
        return "—"
    local = datetime.fromtimestamp(ts, tz=ZoneInfo(tz_name))
    if time_format == "12":
        hour12 = local.strftime("%I").lstrip("0") or "12"
        return f"{hour12}:{local:%M} {local:%p} {local:%Z}".strip()
    return f"{local:%H:%M} {local:%Z}".strip()


def _estimated_return_cell(entry: AfkEntry, now_ts: float) -> str:
    if entry.expected_return_ts is None:
        return "—"

    base = fmt_time(entry.expected_return_ts, entry.tz, entry.time_format)
    if entry.expected_return_ts < now_ts:
        base += f" ⏰ ({format_delta(now_ts - entry.expected_return_ts)} late)"
    if entry.extended and entry.original_expected_return_ts not in (None, entry.expected_return_ts):
        base += f" (original {fmt_time(entry.original_expected_return_ts, entry.tz, entry.time_format)})"
    return base


def _returned_at_cell(entry: AfkEntry) -> str:
    base = fmt_time(entry.returned_ts, entry.tz, entry.time_format)
    if entry.expected_return_ts is None:
        return f"✅ {base}"
    diff = entry.returned_ts - entry.expected_return_ts
    label = "less" if diff <= 0 else "late"
    return f"{base} ✅ ({format_delta(diff)} {label})"


def _back_in_seconds_away(entry: AfkEntry, now_ts: float) -> float | None:
    """Live countdown to the estimated return, relative to now."""
    if entry.expected_return_ts is None:
        return None
    return entry.expected_return_ts - now_ts


def _back_in_seconds_returned(entry: AfkEntry, now_ts: float) -> float:
    """Live "time since actual return" — 0m the moment they're back, - 1m a minute later."""
    return entry.returned_ts - now_ts


def _back_in_cell(seconds: float | None, extended: bool) -> str:
    base = "—" if seconds is None else format_countdown(seconds)
    if extended:
        return f"⏰{base}"
    return base


def _name_cell(entry: AfkEntry, now_ts: float) -> str:
    if entry.returned_ts is not None:
        icon = " ✅"
    elif entry.expected_return_ts is not None and entry.expected_return_ts < now_ts:
        icon = " ⏰"
    else:
        icon = ""

    name_line = f"{entry.name}{icon}"
    if entry.extended and entry.returned_ts is None:
        return f"{name_line}<br>_needs 30 minutes_"
    return name_line


def _render_away_row(entry: AfkEntry, now_ts: float) -> str:
    back_in = _back_in_cell(_back_in_seconds_away(entry, now_ts), entry.extended)
    return (
        f"| {_name_cell(entry, now_ts)} | {back_in} | {fmt_time(entry.start_ts, entry.tz, entry.time_format)} "
        f"| {_estimated_return_cell(entry, now_ts)} | {entry.comment or ''} |"
    )


def _render_returned_row(entry: AfkEntry, now_ts: float) -> str:
    back_in = _back_in_cell(_back_in_seconds_returned(entry, now_ts), extended=False)
    return (
        f"| {_name_cell(entry, now_ts)} | {back_in} | {fmt_time(entry.start_ts, entry.tz, entry.time_format)} "
        f"| {_returned_at_cell(entry)} | {entry.comment or ''} |"
    )


def _render_table(headers: list[str], rows: list[str]) -> str:
    header = f"| {' | '.join(headers)} |\n| {' | '.join(['---'] * len(headers))} |"
    return header + "\n" + "\n".join(rows)


def render_markdown(entries: list[AfkEntry], now: datetime) -> str:
    header_line = f"**Away from keyboard:** {now:%a}, {now:%b}-{now.day}"
    empty_text = "_Weekend._" if now.weekday() >= 5 else "_Everyone's around._"

    away = [e for e in entries if e.returned_ts is None]
    returned = [e for e in entries if e.returned_ts is not None]

    if not away and not returned:
        return "\n\n".join([header_line, "", empty_text])

    now_ts = now.timestamp()
    parts = [header_line]

    if away:
        away.sort(key=lambda e: (v if (v := _back_in_seconds_away(e, now_ts)) is not None else math.inf))
        parts.append(_render_table(_HEADERS_AWAY, [_render_away_row(e, now_ts) for e in away]))
    else:
        parts.append("")
        parts.append(empty_text)

    if returned:
        returned.sort(key=lambda e: _back_in_seconds_returned(e, now_ts), reverse=True)
        parts.append("")
        parts.append("**Back in business:**")
        parts.append(_render_table(_HEADERS_RETURNED, [_render_returned_row(e, now_ts) for e in returned]))

    return "\n\n".join(parts)


async def render_and_push(client: AsyncWebClient, canvas_ids: list[str], entries: list[AfkEntry], now: datetime) -> None:
    markdown = render_markdown(entries, now)
    for canvas_id in canvas_ids:
        await client.canvases_edit(
            canvas_id=canvas_id,
            changes=[
                {
                    "operation": "replace",
                    "document_content": {"type": "markdown", "markdown": markdown},
                }
            ],
        )
