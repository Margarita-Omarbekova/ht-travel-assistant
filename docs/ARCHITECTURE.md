# Architecture

## High-level

Telegram / Web / App
→ Travel Assistant Backend
→ Conversation State + Travel Profile
→ Recommendation Logic + Knowledge Base
→ Tours API / Flights API / Hotels API
→ Offer normalization
→ Ranking & comparison
→ LLM response generation

## Current MVP

- Python
- FastAPI
- Railway
- Telegram Bot API
- OpenAI Responses API
- OpenAI speech-to-text for voice messages
- Supabase planned for persistence

## Responsibility split

### LLM
Использовать для:
- понимания свободного текста;
- извлечения предпочтений;
- уточняющих вопросов;
- объяснения рекомендаций;
- summary.

Не использовать как единственный источник:
- цен;
- наличия;
- расписаний;
- визовых правил;
- сезонных бизнес-правил;
- коммерческой логики.

### Backend
Должен решать:
- состояние диалога;
- что уже известно;
- нужен ли новый вопрос;
- пора ли рекомендовать;
- какой API вызвать;
- как нормализовать ответы;
- как ранжировать офферы.

## Planned integrations

Отдельные adapters:
- services/tours.py
- services/flights.py
- services/hotels.py

Внешние API должны приводиться к общему внутреннему Offer.

Пример полей:
- type
- source
- price
- currency
- destination
- dates
- hotel
- room
- meal
- flight
- baggage
- transfer
- refundable
- booking_url

## Security

Никогда не коммитить:
- API tokens;
- Telegram bot token;
- OpenAI API key;
- cookies;
- session IDs;
- PHPSESSID;
- browser Copy-as-cURL с живой сессией.

Все секреты хранить только в Railway / secret storage.
