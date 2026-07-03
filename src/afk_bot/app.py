import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from afk_bot.config import Config
from afk_bot.handlers import register_handlers
from afk_bot.preferences import PreferencesStore
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.scheduler import start_daily_cleanup, start_overdue_checker
from afk_bot.state import StateStore
from afk_bot.watchers import WatchersStore

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    config = Config()
    app = AsyncApp(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)
    state = StateStore(config.STATE_FILE_PATH)
    prefs = PreferencesStore(config.PREFERENCES_FILE_PATH)
    watchers = WatchersStore(config.WATCHERS_FILE_PATH)
    queue = SingleWriterQueue()
    queue.start()

    register_handlers(app, state, queue, config.CANVAS_IDS, config.DEFAULT_LOCALE, prefs, watchers)

    scheduler = AsyncIOScheduler()
    start_daily_cleanup(
        scheduler,
        state,
        queue,
        app.client,
        config.CANVAS_IDS,
        watchers,
        config.DAILY_CLEANUP_HOUR,
        config.DAILY_CLEANUP_MINUTE,
        config.TIMEZONE,
    )
    start_overdue_checker(
        scheduler,
        state,
        queue,
        app.client,
        config.CANVAS_IDS,
        config.OVERDUE_CHECK_INTERVAL_MINUTES,
    )
    scheduler.start()

    handler = AsyncSocketModeHandler(app, config.SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
