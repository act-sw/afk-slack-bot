import math
from datetime import datetime
from zoneinfo import ZoneInfo

from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.formatting import format_delta
from afk_bot.state import AfkEntry

_HEADERS = ["Name", "AFK since", "Estimated return", "Comment"]


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


def _sort_key(entry: AfkEntry) -> float:
    return entry.expected_return_ts if entry.expected_return_ts is not None else math.inf


def render_markdown(entries: list[AfkEntry], now: datetime) -> str:
    header_line = f"**Away from keyboard** {now.month}/{now.day}"

    if not entries:
        return f"{header_line}\n\n_Everyone's around._"

    now_ts = now.timestamp()
    header = f"| {' | '.join(_HEADERS)} |\n| {' | '.join(['---'] * len(_HEADERS))} |"
    rows = [
        f"| {entry.name} | {fmt_time(entry.start_ts, entry.tz)} | {_return_cell(entry, now_ts)} | {entry.comment or ''} |"
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
