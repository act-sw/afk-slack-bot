# afk-slack-bot

Slack-бот для менеджмента AFK-сообщений команды без отдельного чата в Slack.
Слеш-команда `/afk 1.5h [комментарий]` пишет/обновляет запись в Canvas канала,
`/back` — досрочное возвращение. Раз в сутки список очищается.

Если время возврата истекло, а `/back` не была вызвана, бот раз в
`OVERDUE_CHECK_INTERVAL_MINUTES` шлёт пользователю личное сообщение с кнопкой
"Вернулся" — один клик регистрирует возврат так же, как `/back`.

Текст команд/сообщений локализуется под язык интерфейса вызвавшего Slack-
пользователя (`ru`/`en`, см. `i18n.py`); в канвасе (общем для всех) —
`DEFAULT_LOCALE`. Время в канвасе и в напоминаниях показывается в часовом
поясе конкретного пользователя с аббревиатурой (`16:13 MSK`), а не системном
времени сервера. Имя в канвасе — Slack display name/real name, а не логин.

Стек: Python, [Bolt for Python](https://slack.dev/bolt-python/) в Socket Mode
(не требует публичного HTTPS-эндпоинта).

## Архитектурные инварианты

- **Ровно один инстанс процесса.** Все входящие команды идут через
  single-writer очередь (`queue_worker.py`) — запись в state store и
  перерисовка канваса выполняются как один атомарный шаг. Больше одного
  инстанса/реплики — гонки за канвас.
- State store (`data/state.json`) — источник истины, канвас — просто вьюха,
  перерисовывается целиком при каждом изменении.

## Slack App: необходимые скоупы/настройки

См. также `slack-app-manifest.yml` — актуальный источник правды по скоупам.

- Socket Mode включён, App-Level Token с `connections:write`
- Interactivity включена (нужна для кнопки "Вернулся" в напоминании)
- Bot Token Scopes: `commands`, `canvases:write`, `chat:write`, `users:read`
- Slash-команды: `/afk`, `/back`

При добавлении новых скоупов в уже установленное приложение нужно заново
нажать **Install to Workspace** — токен `SLACK_BOT_TOKEN` при этом меняется.

## Настройка

```bash
cp .env.example .env
# заполнить SLACK_BOT_TOKEN, SLACK_APP_TOKEN, CANVAS_ID
```

## Запуск локально

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m afk_bot.app
```

## Деплой (Docker)

```bash
docker compose up -d --build
```

`docker-compose.yml` держит один реплик — не увеличивать `--scale`, это сломает
no-race гарантию очереди.

## См. также

Полный design doc: `workspace/afk-bot-design-v20260703.md` в родительском
рабочем каталоге разработчика (не часть этого репозитория).
