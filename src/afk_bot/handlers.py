from datetime import datetime

from slack_bolt.async_app import AsyncApp

from afk_bot.canvas_renderer import render_and_push
from afk_bot.duration_parser import ParseError, parse_expected_return
from afk_bot.i18n import resolve_locale, t
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import AfkEntry, StateStore

BACK_BUTTON_ACTION_ID = "afk_back_button"


async def _fetch_user_profile(client, user_id: str, default_locale: str) -> dict:
    info = (await client.users_info(user=user_id, include_locale=True))["user"]
    display_name = info["profile"].get("display_name") or info["real_name"]
    return {
        "name": display_name,
        "tz": info.get("tz") or "UTC",
        "locale": resolve_locale(info.get("locale"), default_locale),
    }


def register_handlers(
    app: AsyncApp, state: StateStore, queue: SingleWriterQueue, canvas_id: str, default_locale: str
) -> None:
    @app.command("/afk")
    async def handle_afk(ack, command, client, respond):
        await ack()
        now = datetime.now()
        text = command["text"].strip()
        duration_text, _, comment = text.partition(" ")
        profile = await _fetch_user_profile(client, command["user_id"], default_locale)

        try:
            expected_return_ts = parse_expected_return(duration_text, now)
        except ParseError as exc:
            await respond(t(profile["locale"], "parse_error", text=exc.text))
            return

        async def job():
            entry = AfkEntry(
                user_id=command["user_id"],
                name=profile["name"],
                start_ts=now.timestamp(),
                expected_return_ts=expected_return_ts.timestamp() if expected_return_ts else None,
                comment=comment.strip(),
                tz=profile["tz"],
                locale=profile["locale"],
            )
            state.upsert(entry)
            await render_and_push(client, canvas_id, state.all(), datetime.now(), default_locale)

        await queue.submit(job)
        duration_label = duration_text or t(profile["locale"], "afk_no_duration")
        await respond(t(profile["locale"], "afk_confirmation", duration=duration_label))

    @app.command("/back")
    async def handle_back(ack, command, client, respond):
        await ack()
        profile = await _fetch_user_profile(client, command["user_id"], default_locale)

        async def job():
            removed = state.remove(command["user_id"])
            if removed:
                await render_and_push(client, canvas_id, state.all(), datetime.now(), default_locale)
            return removed

        removed = await queue.submit(job)
        key = "back_confirmation" if removed else "back_not_afk"
        await respond(t(profile["locale"], key))

    @app.action(BACK_BUTTON_ACTION_ID)
    async def handle_back_button(ack, body, client):
        await ack()
        user_id = body["user"]["id"]
        locale = resolve_locale(body["user"].get("locale"), default_locale)

        async def job():
            removed = state.remove(user_id)
            if removed:
                await render_and_push(client, canvas_id, state.all(), datetime.now(), default_locale)
            return removed

        await queue.submit(job)
        await client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=t(locale, "overdue_dm_resolved"),
            blocks=[],
        )
