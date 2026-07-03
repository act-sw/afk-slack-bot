import dataclasses
from datetime import datetime

from slack_bolt.async_app import AsyncApp

from afk_bot.canvas_renderer import render_and_push
from afk_bot.duration_parser import parse_afk_text
from afk_bot.formatting import format_delta
from afk_bot.i18n import LANGUAGE_NAMES, SUPPORTED_LOCALES, resolve_locale, t
from afk_bot.preferences import PreferencesStore
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import AfkEntry, StateStore

BACK_BUTTON_ACTION_ID = "afk_back_button"

_LANGUAGE_OPTIONS = ", ".join(SUPPORTED_LOCALES)


async def _fetch_user_profile(client, user_id: str, default_locale: str, prefs: PreferencesStore) -> dict:
    info = (await client.users_info(user=user_id, include_locale=True))["user"]
    display_name = info["profile"].get("display_name") or info["real_name"]
    locale = prefs.get_locale(user_id) or resolve_locale(info.get("locale"), default_locale)
    return {
        "name": display_name,
        "tz": info.get("tz") or "UTC",
        "locale": locale,
    }


def register_handlers(
    app: AsyncApp,
    state: StateStore,
    queue: SingleWriterQueue,
    canvas_ids: list[str],
    default_locale: str,
    prefs: PreferencesStore,
) -> None:
    @app.command("/afk")
    async def handle_afk(ack, command, client, respond):
        await ack()
        now = datetime.now()
        profile = await _fetch_user_profile(client, command["user_id"], default_locale, prefs)
        expected_return, comment = parse_afk_text(command["text"], now)

        async def job():
            entry = AfkEntry(
                user_id=command["user_id"],
                name=profile["name"],
                start_ts=now.timestamp(),
                expected_return_ts=expected_return.timestamp() if expected_return else None,
                comment=comment,
                tz=profile["tz"],
                locale=profile["locale"],
            )
            state.upsert(entry)
            await render_and_push(client, canvas_ids, state.all(), datetime.now())

        await queue.submit(job)
        if expected_return:
            duration_label = format_delta((expected_return - now).total_seconds())
        else:
            duration_label = t(profile["locale"], "afk_no_duration")
        await respond(t(profile["locale"], "afk_confirmation", duration=duration_label))

    @app.command("/back")
    async def handle_back(ack, command, client, respond):
        await ack()
        profile = await _fetch_user_profile(client, command["user_id"], default_locale, prefs)

        async def job():
            entry = state.get(command["user_id"])
            if entry is None or entry.returned_ts is not None:
                return False
            state.upsert(dataclasses.replace(entry, returned_ts=datetime.now().timestamp()))
            await render_and_push(client, canvas_ids, state.all(), datetime.now())
            return True

        marked = await queue.submit(job)
        key = "back_confirmation" if marked else "back_not_afk"
        await respond(t(profile["locale"], key))

    @app.command("/afk-lang")
    async def handle_afk_lang(ack, command, respond):
        await ack()
        raw = command["text"].strip().lower()
        current_locale = prefs.get_locale(command["user_id"]) or default_locale

        if not raw:
            await respond(
                t(current_locale, "lang_current", name=LANGUAGE_NAMES[current_locale], options=_LANGUAGE_OPTIONS)
            )
            return

        if raw not in SUPPORTED_LOCALES:
            await respond(t(current_locale, "lang_invalid", input=raw, options=_LANGUAGE_OPTIONS))
            return

        async def job():
            prefs.set_locale(command["user_id"], raw)

        await queue.submit(job)
        await respond(t(raw, "lang_set", name=LANGUAGE_NAMES[raw]))

    @app.action(BACK_BUTTON_ACTION_ID)
    async def handle_back_button(ack, body, client):
        await ack()
        user_id = body["user"]["id"]
        locale = prefs.get_locale(user_id) or resolve_locale(body["user"].get("locale"), default_locale)

        async def job():
            entry = state.get(user_id)
            if entry is None or entry.returned_ts is not None:
                return False
            state.upsert(dataclasses.replace(entry, returned_ts=datetime.now().timestamp()))
            await render_and_push(client, canvas_ids, state.all(), datetime.now())
            return True

        marked = await queue.submit(job)
        key = "overdue_dm_resolved" if marked else "back_not_afk"
        await client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=t(locale, key),
            blocks=[],
        )
