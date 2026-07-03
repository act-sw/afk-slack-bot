from datetime import datetime

from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.state import AfkEntry

_HEADER = "| Имя | Ушёл в | Вернётся ~ | Комментарий |\n| --- | --- | --- | --- |"


def _fmt_time(ts: float | None) -> str:
    if ts is None:
        return "—"
    return datetime.fromtimestamp(ts).strftime("%H:%M")


def render_markdown(entries: list[AfkEntry], now: datetime) -> str:
    if not entries:
        return "_Сейчас все на месте._"

    rows = []
    for entry in sorted(entries, key=lambda e: e.start_ts):
        overdue = entry.expected_return_ts is not None and entry.expected_return_ts < now.timestamp()
        return_cell = _fmt_time(entry.expected_return_ts)
        if overdue:
            return_cell = f"⏰ _задержался ({return_cell})_"
        rows.append(f"| {entry.name} | {_fmt_time(entry.start_ts)} | {return_cell} | {entry.comment or ''} |")

    return _HEADER + "\n" + "\n".join(rows)


async def render_and_push(client: AsyncWebClient, canvas_id: str, entries: list[AfkEntry], now: datetime) -> None:
    markdown = render_markdown(entries, now)
    await client.canvases_edit(
        canvas_id=canvas_id,
        changes=[
            {
                "operation": "replace",
                "document_content": {"type": "markdown", "markdown": markdown},
            }
        ],
    )
