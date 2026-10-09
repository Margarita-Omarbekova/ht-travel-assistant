# HT Travel Assistant

MVP Telegram-бота для проекта HT Travel Assistant.

## Реализовано

- FastAPI backend
- Telegram webhook
- `/start`
- `/favorites`
- `/history`
- `/manager`
- обычный диалог через OpenAI Responses API
- временная память текущего диалога

## Railway variables

Добавить в Railway → Variables:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_MODEL` = `gpt-5-mini`
- `WEBHOOK_SECRET` = любая длинная случайная строка из латинских букв, цифр, `_` и `-`

## Start command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## После deploy

1. Railway → Settings → Networking → Generate Domain.
2. Зарегистрировать Telegram webhook на:
   `https://<railway-domain>/telegram/webhook`
3. Передать тот же `WEBHOOK_SECRET` при регистрации webhook.

## Следующий этап

- Supabase
- сохранённые планы
- история путешествий
- структурированный travel profile
- база знаний по сезонности/регионам
- передача менеджеру
