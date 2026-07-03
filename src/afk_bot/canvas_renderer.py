from datetime import datetime
from zoneinfo import ZoneInfo

from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.i18n import t
from afk_bot.state import AfkEntry


def fmt_time(ts: float | None, tz_name: str) -> str:
    if ts is None:
        return "—"
    local = datetime.fromtimestamp(ts, tz=ZoneInfo(tz_name))
    return f"{local:%H:%M} {local:%Z}".strip()


def render_markdown(entries: list[AfkEntry], now: datetime, locale: str) -> str:
    if not entries:
        return t(locale, "canvas_empty")

    header_cells = t(locale, "canvas_headers")
    header = f"| {' | '.join(header_cells)} |\n| {' | '.join(['---'] * len(header_cells))} |"

    rows = []
    for entry in sorted(entries, key=lambda e: e.start_ts):
        overdue = entry.expected_return_ts is not None and entry.expected_return_ts < now.timestamp()
        return_cell = fmt_time(entry.expected_return_ts, entry.tz)
        if overdue:
            return_cell = f"{t(locale, 'canvas_overdue_marker')} _({return_cell})_"
        rows.append(
            f"| {entry.name} | {fmt_time(entry.start_ts, entry.tz)} | {return_cell} | {entry.comment or ''} |"
        )

    return header + "\n" + "\n".join(rows)


async def render_and_push(
    client: AsyncWebClient, canvas_id: str, entries: list[AfkEntry], now: datetime, locale: str
) -> None:
    markdown = render_markdown(entries, now, locale)
    await client.canvases_edit(
        canvas_id=canvas_id,
        changes=[
            {
                "operation": "replace",
                "document_content": {"type": "markdown", "markdown": markdown},
            }
        ],
    )
