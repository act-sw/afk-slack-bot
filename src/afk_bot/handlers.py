import dataclasses
import re
from datetime import datetime

from slack_bolt.async_app import AsyncApp

from afk_bot.canvas_renderer import render_and_push
from afk_bot.duration_parser import parse_afk_text
from afk_bot.formatting import format_duration_words
from afk_bot.i18n import LANGUAGE_NAMES, SUPPORTED_LOCALES, resolve_locale, t
from afk_bot.preferences import PreferencesStore
from afk_bot.queue_worker import SingleWriterQueue
from afk_bot.state import AfkEntry, StateStore
from afk_bot.watchers import WatchersStore

BACK_BUTTON_ACTION_ID = "afk_back_button"

_LANGUAGE_OPTIONS = ", ".join(SUPPORTED_LOCALES)
_MENTION_RE = re.compile(r"<@([A-Z0-9]+)(?:\|[^>]*)?>")


async def _fetch_user_profile(client, user_id: str, default_locale: str, prefs: PreferencesStore) -> dict:
    info = (await client.users_info(user=user_id, include_locale=True))["user"]
    display_name = info["profile"].get("display_name") or info["real_name"]
    locale = prefs.get_locale(user_id) or resolve_locale(info.get("locale"), default_locale)
    return {
        "name": display_name,
        "tz": info.get("tz") or "UTC",
        "locale": locale,
    }


def _build_return_message(entry: AfkEntry, locale: str) -> str:
    duration = format_duration_words(entry.returned_ts - entry.start_ts, locale)
    if entry.expected_return_ts is None:
        return t(locale, "back_confirmation_no_delta", duration=duration)

    diff = entry.returned_ts - entry.expected_return_ts
    delta_key = "delta_less" if diff <= 0 else "delta_more"
    delta = t(locale, delta_key, amount=format_duration_words(abs(diff), locale))
    return t(locale, "back_confirmation_with_delta", duration=duration, delta=delta)


def register_handlers(
    app: AsyncApp,
    state: StateStore,
    queue: SingleWriterQueue,
    canvas_ids: list[str],
    default_locale: str,
    prefs: PreferencesStore,
    watchers: WatchersStore,
) -> None:
    async def mark_returned(user_id: str, client) -> AfkEntry | None:
        async def job():
            entry = state.get_active(user_id)
            if entry is None:
                return None
            updated = dataclasses.replace(entry, returned_ts=datetime.now().timestamp())
            state.upsert(updated)
            await render_and_push(client, canvas_ids, state.all(), datetime.now())
            return updated

        updated_entry = await queue.submit(job)
        if updated_entry is not None:
            for watcher_id in watchers.pop_all(user_id):
                watcher_profile = await _fetch_user_profile(client, watcher_id, default_locale, prefs)
                await client.chat_postMessage(
                    channel=watcher_id,
                    text=t(watcher_profile["locale"], "wait_notification", name=updated_entry.name),
                )
        return updated_entry

    async def do_afk(text: str, command, client, respond):
        now = datetime.now()
        user_id = command["user_id"]
        profile = await _fetch_user_profile(client, user_id, default_locale, prefs)
        expected_return, comment = parse_afk_text(text, now)

        async def job():
            active = state.get_active(user_id)
            entry_id = active.entry_id if active else f"{user_id}-{int(now.timestamp() * 1000)}"
            entry = AfkEntry(
                entry_id=entry_id,
                user_id=user_id,
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
            duration = format_duration_words((expected_return - now).total_seconds(), profile["locale"])
            message = t(profile["locale"], "afk_confirmation_duration", duration=duration)
        else:
            message = t(profile["locale"], "afk_confirmation_open")
        await respond(message)

    async def do_back(command, client, respond):
        profile = await _fetch_user_profile(client, command["user_id"], default_locale, prefs)
        entry = await mark_returned(command["user_id"], client)
        message = _build_return_message(entry, profile["locale"]) if entry else t(profile["locale"], "back_not_afk")
        await respond(message)

    async def do_lang(text: str, command, respond):
        raw = text.strip().lower()
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

    async def do_wait(text: str, command, respond):
        profile_locale = prefs.get_locale(command["user_id"]) or default_locale
        target_ids = _MENTION_RE.findall(text)
        if not target_ids:
            await respond(t(profile_locale, "wait_no_mentions"))
            return

        async def job():
            for target_id in target_ids:
                watchers.add(target_id, command["user_id"])

        await queue.submit(job)
        mentions = " ".join(f"<@{uid}>" for uid in target_ids)
        await respond(t(profile_locale, "wait_confirmation", mentions=mentions))

    @app.command("/afk")
    async def handle_afk_command(ack, command, client, respond):
        await ack()
        text = command["text"].strip()
        first_word, _, rest = text.partition(" ")
        subcommand = first_word.lower()

        if subcommand == "back":
            await do_back(command, client, respond)
        elif subcommand == "lang":
            await do_lang(rest, command, respond)
        elif subcommand == "wait":
            await do_wait(rest, command, respond)
        else:
            await do_afk(text, command, client, respond)

    @app.action(BACK_BUTTON_ACTION_ID)
    async def handle_back_button(ack, body, client):
        await ack()
        user_id = body["user"]["id"]
        active_before = state.get_active(user_id)
        locale = active_before.locale if active_before else (prefs.get_locale(user_id) or default_locale)

        entry = await mark_returned(user_id, client)
        message = _build_return_message(entry, locale) if entry else t(locale, "back_not_afk")
        await client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=message,
            blocks=[],
        )
