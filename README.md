# afk-slack-bot

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12%2B-brightgreen)
![Slack Bolt](https://img.shields.io/badge/Slack-Bolt%20for%20Python-4A154B)

A Slack bot for tracking who's away from keyboard, without needing a dedicated
channel for it. Everything lives in one `/afk` slash command with
subcommands, and a live-updating Canvas that the whole team can glance at.

## 📖 Description

Instead of a channel full of "brb 15 min" messages, `afk-slack-bot` keeps a
single shared Canvas with two tables — who's currently away (sorted by
soonest back) and who's already back (sorted by most recently returned).
Every AFK, return, or extension is reflected there within a minute, in each
viewer's own timezone and time format.

The bot runs in Socket Mode, so it needs no public HTTPS endpoint — just a
Slack app with a bot token and an app-level token.

## ✨ Features

- **One command, several subcommands**: `/afk`, `/afk back`, `/afk lang`,
  `/afk format`, `/afk wait`, `/afk help`.
- **Flexible duration parsing**: `/afk 1.5`, `/afk 90`, `/afk 13h`,
  `/afk until 14:00`, or an open-ended `/afk lunch` with no time at all.
- **Per-user locale and time format**: language defaults to the user's own
  Slack interface language (overridable), time format defaults to 24-hour.
  Six locales are bundled: `ru`, `en`, `pl`, `uk`, `be`, `es`, with correct
  Slavic pluralization and grammatical case for duration phrases.
- **Overdue reminders**: if the expected return time passes without
  `/afk back`, the bot DMs the person a one-time reminder with two buttons —
  "I'm here" and "I need 30 more minutes" — and reflects the extension on the
  Canvas (⏰ marker, original ETA kept in parentheses).
- **`/afk wait @user`**: get DMed when someone you're waiting on returns (or
  needs more time); the watched person is notified too, so they know someone
  is waiting.
- **Multiple Canvases**: the same state can be mirrored to several Canvases
  at once (e.g. one per channel), configured via a comma-separated list.

## 🚀 Commands

- `/afk N[unit] [comment]` — mark yourself away. Without a unit, `N ≤ 12` is
  read as hours and `N > 12` as minutes; an explicit unit overrides that
  guess — `h`/`hr`/`hour`, `ч`/`час`, `год`/`година` (Ukrainian "год" is an
  hour, not a year!), `godz`/`godzina`, `hora` for hours, `m`/`min`/`minute`,
  `мин`, `хв`/`хвилина`, `minut`/`minuta` for minutes. Fractional values are
  accepted (`,` or `.` as the decimal separator) and round up to a whole
  minute. Everything after the number (and unit, if recognized) becomes a
  free-form comment. With no number at all, it's an open-ended AFK and the
  whole text becomes the comment.
- `/afk until <time> [comment]` — away until a specific time, in the user's
  **own** timezone. Accepts `14`, `1400`, `14:00`, or a 12-hour value with an
  `am`/`pm` suffix (`2pm`, `2:30am`). A bare `H:MM` clock time (e.g. `23:55`,
  `2:30pm`) is also recognized without the `until` keyword, since a plain
  duration number never contains a colon. Without an am/pm suffix, an hour
  in 1–12 is ambiguous — the bot resolves it to whichever of the two
  12-hour readings comes soonest (`until 2` at 10:00 means 14:00 today; the
  same command at 15:00 means 02:00 the next day, since 14:00 has already
  passed).
- `/afk back` — mark your return.
- `/afk lang [ru|en|pl|uk|be|es]` — set the bot's reply language for you
  (no argument shows the current one).
- `/afk format [12|24]` — set the time display format everywhere (no
  argument shows the current one; defaults to 24-hour).
- `/afk wait @user [@user2 ...]` — get a DM when the mentioned people mark
  their return (or need more time); they get a heads-up DM too.
- `/afk help` — a short command reference.

Examples: `/afk 1.5 lunch` · `/afk 90` · `/afk 13h` · `/afk until 14` ·
`/afk until 2pm` · `/afk back` · `/afk lang en` · `/afk format 12` ·
`/afk wait @name`.

## 🖼 The Canvas

Two tables: active AFKs (sorted ascending by "Back in") and "**Back in
business:**" — people who already returned, kept as history rather than
deleted (sorted descending by how long ago they returned). If someone goes
AFK again later the same day, it's a new row, not an overwrite of the old
one. All entries — active and returned — are cleared once a day
(`DAILY_CLEANUP_HOUR`/`DAILY_CLEANUP_MINUTE`, in `TIMEZONE`; defaults to
4:00 UTC). The Canvas re-renders every minute on the `:00` boundary, plus
immediately on any event (`/afk`, `/afk back`, button clicks).

Times are shown in each person's own timezone with its abbreviation (e.g.
`16:13 MSK`), never the server's local time. Names shown are the Slack
display name / real name, not the account handle. The Canvas content itself
is always in English regardless of each user's chosen bot language — it's a
shared view, not a personal one.

## 🌍 Localization

Command replies and DMs are localized per user: the default is the language
of that user's own Slack client, overridable with `/afk lang`. Six locales
ship out of the box — Russian, English, Polish, Ukrainian, Belarusian,
Spanish — including correct Slavic pluralization (one/few/many forms) and
grammatical case for duration phrases (e.g. "за 41 минуту" vs "за 45
минут").

## 🏗 Architectural invariants

- **Exactly one running instance.** Every incoming command goes through a
  single-writer queue (`queue_worker.py`) — the state-store write and the
  Canvas re-render happen as one atomic step. Running more than one
  instance/replica would race on the Canvas.
- The JSON state store (`data/state.json`) is the source of truth; the
  Canvas is just a view, fully re-rendered from state on every change.
- A watchdog hard-exits the process if the queue worker is stuck on a single
  job for more than 3 minutes (covers hangs that don't respond to
  cancellation, e.g. a poisoned connection pool after a network blip) —
  paired with Docker's `restart: unless-stopped`, this makes the bot
  self-heal within minutes instead of requiring a manual restart.

## 🔧 Slack App setup

See `slack-app-manifest.yml` for the source of truth on scopes and settings
(the manifest editor in Slack's web UI can mangle indentation on paste —
it's more reliable to configure these by hand: OAuth & Permissions /
Interactivity & Shortcuts / Slash Commands).

- Socket Mode enabled, with an App-Level Token that has `connections:write`
- Interactivity enabled (needed for the reminder buttons)
- Bot Token Scopes: `commands`, `canvases:write`, `chat:write`, `users:read`
- Slash command `/afk`, with "Escape channels, users, and links sent to
  your app" enabled (needed for `/afk wait @user` — otherwise Slack won't
  expand `@user` into `<@ID>` and the bot can't resolve the mention)

After adding new scopes to an already-installed app, you need to click
**Install to Workspace** again — this rotates `SLACK_BOT_TOKEN`.

## ⚙️ Configuration

```bash
cp .env.example .env
# fill in SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET, CANVAS_IDS
```

`CANVAS_IDS` is a comma-separated list of Canvas IDs. A Canvas's ID is the
last segment of its link (Open canvas in new tab / share link on the
Canvas): `https://<workspace>.slack.com/docs/<TEAM_ID>/<CANVAS_ID>`.

## 🖥 Running locally

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m afk_bot.app
```

## 🐳 Deployment (Docker)

```bash
docker compose up -d --build
```

`docker-compose.yml` runs a single replica — don't scale it up, that would
break the queue's no-race guarantee.

## 📄 License

MIT — see [LICENSE](LICENSE).
