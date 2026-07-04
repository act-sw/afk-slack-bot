import math
from datetime import datetime
from zoneinfo import ZoneInfo

from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.formatting import format_countdown, format_delta
from afk_bot.state import AfkEntry

_HEADERS = ["Name", "Back in", "AFK since", "Estimated return", "Comment"]


def fmt_time(ts: float | None, tz_name: str) -> str:
    if ts is None:
        return "—"
    local = datetime.fromtimestamp(ts, tz=ZoneInfo(tz_name))
    return f"{local:%H:%M} {local:%Z}".strip()


def _return_cell(entry: AfkEntry, now_ts: float) -> str:
    base = fmt_time(entry.expected_return_ts, entry.tz)

    if entry.returned_ts is not None:
        if entry.expected_return_ts is None:
            return f"✅ {fmt_time(entry.returned_ts, entry.tz)}"
        diff = entry.returned_ts - entry.expected_return_ts
        label = "less" if diff <= 0 else "late"
        return f"{base} ✅ ({format_delta(diff)} {label})"

    if entry.expected_return_ts is not None and entry.expected_return_ts < now_ts:
        return f"{base} ⏰ ({format_delta(now_ts - entry.expected_return_ts)} late)"

    return base


def _back_in_cell(entry: AfkEntry, now_ts: float) -> str:
    if entry.expected_return_ts is None:
        base = "—"
    else:
        reference_ts = entry.returned_ts if entry.returned_ts is not None else now_ts
        base = format_countdown(entry.expected_return_ts - reference_ts)
    if entry.extended and entry.returned_ts is None:
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


def _sort_key(entry: AfkEntry) -> float:
    return entry.expected_return_ts if entry.expected_return_ts is not None else math.inf


def render_markdown(entries: list[AfkEntry], now: datetime) -> str:
    header_line = f"**Away from keyboard:** {now:%a}, {now:%b}-{now.day}"

    if not entries:
        empty_text = "_Weekend._" if now.weekday() >= 5 else "_Everyone's around._"
        return f"{header_line}\n\n{empty_text}"

    now_ts = now.timestamp()
    header = f"| {' | '.join(_HEADERS)} |\n| {' | '.join(['---'] * len(_HEADERS))} |"
    rows = [
        f"| {_name_cell(entry, now_ts)} | {_back_in_cell(entry, now_ts)} | {fmt_time(entry.start_ts, entry.tz)} "
        f"| {_return_cell(entry, now_ts)} | {entry.comment or ''} |"
        for entry in sorted(entries, key=_sort_key)
    ]

    return header_line + "\n\n" + header + "\n" + "\n".join(rows)


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
