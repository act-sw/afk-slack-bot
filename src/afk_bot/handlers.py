from datetime import datetime

from slack_bolt.async_app import AsyncApp

from afk_bot.canvas_renderer import render_and_push
from afk_bot.duration_parser import ParseError, parse_expected_return
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import AfkEntry, StateStore


def register_handlers(app: AsyncApp, state: StateStore, queue: SingleWriterQueue, canvas_id: str) -> None:
    @app.command("/afk")
    async def handle_afk(ack, command, client, respond):
        await ack()
        now = datetime.now()
        text = command["text"].strip()
        duration_text, _, comment = text.partition(" ")

        try:
            expected_return_ts = parse_expected_return(duration_text, now)
        except ParseError as exc:
            await respond(str(exc))
            return

        async def job():
            entry = AfkEntry(
                user_id=command["user_id"],
                name=command["user_name"],
                start_ts=now.timestamp(),
                expected_return_ts=expected_return_ts.timestamp() if expected_return_ts else None,
                comment=comment.strip(),
            )
            state.upsert(entry)
            await render_and_push(client, canvas_id, state.all(), datetime.now())

        await queue.submit(job)
        await respond(f"Отмечено: отошёл ({duration_text or 'без указания времени'}).")

    @app.command("/back")
    async def handle_back(ack, command, client, respond):
        await ack()

        async def job():
            removed = state.remove(command["user_id"])
            if removed:
                await render_and_push(client, canvas_id, state.all(), datetime.now())
            return removed

        removed = await queue.submit(job)
        await respond("С возвращением!" if removed else "Ты и не отмечался как отошедший.")
