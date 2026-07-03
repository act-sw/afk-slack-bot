import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    CANVAS_IDS = [c.strip() for c in os.environ["CANVAS_IDS"].split(",") if c.strip()]
    STATE_FILE_PATH = os.environ.get("STATE_FILE_PATH", "data/state.json")
    PREFERENCES_FILE_PATH = os.environ.get("PREFERENCES_FILE_PATH", "data/preferences.json")
    WATCHERS_FILE_PATH = os.environ.get("WATCHERS_FILE_PATH", "data/watchers.json")
    TIMEZONE = os.environ.get("TIMEZONE", "UTC")
    DAILY_CLEANUP_HOUR = int(os.environ.get("DAILY_CLEANUP_HOUR", "4"))
    DAILY_CLEANUP_MINUTE = int(os.environ.get("DAILY_CLEANUP_MINUTE", "0"))
    DEFAULT_LOCALE = os.environ.get("DEFAULT_LOCALE", "ru")
    OVERDUE_CHECK_INTERVAL_MINUTES = int(os.environ.get("OVERDUE_CHECK_INTERVAL_MINUTES", "5"))
