import dataclasses
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.canvas_renderer import fmt_time, render_and_push
from afk_bot.handlers import BACK_BUTTON_ACTION_ID
from afk_bot.i18n import t
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import StateStore


def start_daily_cleanup(
    scheduler: AsyncIOScheduler,
    state: StateStore,
    queue: SingleWriterQueue,
    client: AsyncWebClient,
    canvas_ids: list[str],
    hour: int,
    minute: int,
    timezone: str,
) -> None:
    async def cleanup_job():
        state.clear()
        await render_and_push(client, canvas_ids, state.all(), datetime.now())

    async def run_cleanup_job():
        await queue.submit(cleanup_job)

    scheduler.add_job(
        run_cleanup_job,
        trigger=CronTrigger(hour=hour, minute=minute, timezone=timezone),
        id="daily_afk_cleanup",
        replace_existing=True,
    )


def start_overdue_checker(
    scheduler: AsyncIOScheduler,
    state: StateStore,
    queue: SingleWriterQueue,
    client: AsyncWebClient,
    canvas_ids: list[str],
    interval_minutes: int,
) -> None:
    async def check_job():
        now_ts = datetime.now().timestamp()
        entries = state.all()
        for entry in entries:
            if (
                entry.notified
                or entry.returned_ts is not None
                or entry.expected_return_ts is None
                or entry.expected_return_ts >= now_ts
            ):
                continue
            await client.chat_postMessage(
                channel=entry.user_id,
                text=t(entry.locale, "overdue_dm_text", time=fmt_time(entry.expected_return_ts, entry.tz)),
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": t(
                                entry.locale, "overdue_dm_text", time=fmt_time(entry.expected_return_ts, entry.tz)
                            ),
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": t(entry.locale, "overdue_button_label")},
                                "style": "primary",
                                "action_id": BACK_BUTTON_ACTION_ID,
                            }
                        ],
                    },
                ],
            )
            state.upsert(dataclasses.replace(entry, notified=True))

        if entries:
            await render_and_push(client, canvas_ids, state.all(), datetime.now())

    async def run_check_job():
        await queue.submit(check_job)

    scheduler.add_job(
        run_check_job,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id="afk_overdue_checker",
        replace_existing=True,
    )
