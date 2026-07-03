from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.canvas_renderer import render_and_push
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import StateStore


def start_daily_cleanup(
    scheduler: AsyncIOScheduler,
    state: StateStore,
    queue: SingleWriterQueue,
    client: AsyncWebClient,
    canvas_id: str,
    hour: int,
    minute: int,
    timezone: str,
) -> None:
    async def cleanup_job():
        state.clear()
        await render_and_push(client, canvas_id, state.all(), datetime.now())

    scheduler.add_job(
        lambda: queue.submit(cleanup_job),
        trigger=CronTrigger(hour=hour, minute=minute, timezone=timezone),
        id="daily_afk_cleanup",
        replace_existing=True,
    )
