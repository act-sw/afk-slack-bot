import dataclasses
import logging
from datetime import datetime

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from slack_sdk.web.async_client import AsyncWebClient

from afk_bot.canvas_renderer import fmt_time, render_and_push
from afk_bot.handlers import BACK_BUTTON_ACTION_ID, EXTEND_BUTTON_ACTION_ID
from afk_bot.i18n import t
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import StateStore
from afk_bot.watchers import WatchersStore


def start_daily_cleanup(
    scheduler: AsyncIOScheduler,
    state: StateStore,
    queue: SingleWriterQueue,
    client: AsyncWebClient,
    canvas_ids: list[str],
    watchers: WatchersStore,
    hour: int,
    minute: int,
    timezone: str,
) -> None:
    async def cleanup_job():
        state.clear()
        watchers.clear()
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
            reminder_text = t(
                entry.locale,
                "overdue_dm_text",
                time=fmt_time(entry.expected_return_ts, entry.tz, entry.time_format),
            )
            await client.chat_postMessage(
                channel=entry.user_id,
                text=reminder_text,
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": reminder_text}},
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": t(entry.locale, "overdue_button_label")},
                                "style": "primary",
                                "action_id": BACK_BUTTON_ACTION_ID,
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": t(entry.locale, "extend_button_label")},
                                "action_id": EXTEND_BUTTON_ACTION_ID,
                            },
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
        trigger=CronTrigger(second=0),
        id="afk_overdue_checker",
        replace_existing=True,
    )


def start_heartbeat(scheduler: AsyncIOScheduler, url: str, interval_seconds: int = 60) -> None:
    """Ping an external liveness monitor (Uptime Kuma push URL) on a fixed interval.

    Runs outside the single-writer queue on purpose: the heartbeat must keep
    going even if the queue is wedged, so that a stuck queue shows up as a
    missing heartbeat rather than being masked by it. Failures are logged and
    swallowed - monitoring must never take the bot down.
    """
    if not url:
        return

    log = logging.getLogger(__name__)

    async def heartbeat_job():
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    if response.status >= 400:
                        log.warning("heartbeat: monitor returned HTTP %s", response.status)
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see docstring
            log.warning("heartbeat: %s", exc)

    scheduler.add_job(
        heartbeat_job,
        trigger=IntervalTrigger(seconds=interval_seconds),
        id="afk_heartbeat",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
