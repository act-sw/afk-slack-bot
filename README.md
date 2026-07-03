# afk-slack-bot

Slack-бот для менеджмента AFK-сообщений команды без отдельного чата в Slack.
Слеш-команда `/afk 1.5h [комментарий]` пишет/обновляет запись в Canvas канала,
`/back` — досрочное возвращение. Раз в сутки список очищается.

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

- Socket Mode включён, App-Level Token с `connections:write`
- Bot Token Scopes: `commands`, `canvases:write`
- Slash-команды: `/afk`, `/back`

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
