# Codex Handoff

## Роль Codex в проекте

Этот репозиторий — source of truth для разработки HT Travel Assistant.

Не использовать историю чата как единственный источник требований.
Перед изменениями читать:
1. docs/PRODUCT_CONTEXT.md
2. docs/TRAVEL_PROFILE.md
3. docs/ARCHITECTURE.md
4. docs/DATA_SOURCE_DB_HT.md
5. docs/DVHT_CODEX_CONTEXT.md
6. README.md

## Текущее состояние

Рабочий Telegram MVP уже развёрнут на Railway.

Реализовано:
- webhook Telegram;
- /start;
- /favorites placeholder;
- /history placeholder;
- /manager placeholder;
- текстовый диалог через OpenAI;
- voice message transcription;
- временная in-memory conversation history.

## Ближайшие задачи

### 1. Persistence
Подключить Supabase.

Хранить:
- users
- travel_sessions
- travel_profile
- favorites
- completed_trips
- conversation summaries

### 2. Travel Profile
Перевести диалог из “просто chat history” в structured state.

После каждого сообщения:
- извлечь новые факты;
- обновить profile;
- определить missing critical fields;
- решить, нужен ли вопрос или можно рекомендовать.

### 3. Recommendation layer
Не полагаться только на знания LLM.

Добавить структуру для:
- destination knowledge;
- seasonality;
- traveler fit;
- region/resort rules.

### 4. db.ht.kz adapter
Исследование показало:
- hotel page доступна по hotel_id;
- данные приходят в HTML;
- comments table можно парсить;
- production auth пока не определён.

Не использовать browser cookies в production.

### 5. Product APIs
После получения Swagger/tokens подключить:
- tours API;
- flights API;
- hotels API.

Нормализовать ответы в общий Offer.

### 6. Website
Backend проектировать channel-agnostic.
Telegram — только первый клиент.
Сайт должен использовать то же ядро Travel Assistant.

## Coding principles

- secrets only via env;
- no credentials in repo;
- small adapters;
- typed models;
- separation of conversation, recommendation, data access and presentation;
- external facts must be traceable to source;
- avoid putting business rules solely in prompts.
