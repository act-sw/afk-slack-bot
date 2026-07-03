import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    CANVAS_ID = os.environ["CANVAS_ID"]
    STATE_FILE_PATH = os.environ.get("STATE_FILE_PATH", "data/state.json")
    TIMEZONE = os.environ.get("TIMEZONE", "UTC")
    DAILY_CLEANUP_HOUR = int(os.environ.get("DAILY_CLEANUP_HOUR", "0"))
    DAILY_CLEANUP_MINUTE = int(os.environ.get("DAILY_CLEANUP_MINUTE", "0"))
