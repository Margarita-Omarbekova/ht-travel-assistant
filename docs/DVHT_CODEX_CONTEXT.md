# DVHT / db.ht.kz — Codex Working Context

## Назначение

Этот документ описывает уже проверенный способ работы с внутренней админкой:

https://db.ht.kz

Основной кейс: получение точных данных по отелю по внутреннему `hotel_id`.

## Точная карточка отеля

URL:

```
https://db.ht.kz/tours/hotel/update/id/{hotel_id}
```

Проверенный пример:

```
https://db.ht.kz/tours/hotel/update/id/1418
```

Использовать именно карточку по ID, а не поиск по названию, когда нужна точная сущность.

## Что уже проверено

1. Карточка отеля загружается серверным HTML.
2. Основные данные отеля находятся прямо в HTML.
3. Комментарии менеджеров тоже находятся прямо в HTML.
4. Отдельного публичного JSON endpoint для этих данных в проверенном сценарии не обнаружено.
5. Авторизация страницы идёт через browser session cookies, включая `PHPSESSID`.
6. Bearer-token для этой страницы не использовался.
7. Copy as cURL из DevTools успешно получает полный HTML карточки.
8. HTML можно сохранить локально и парсить.

## Как воспроизвести вручную

### 1. Получить авторизованный запрос

В Chrome:
- открыть нужную карточку отеля;
- DevTools → Network;
- выбрать основной `Doc` request страницы;
- Copy → Copy as cURL.

ВАЖНО:
- cURL содержит живые cookies текущей сессии;
- не вставлять его в GitHub;
- не вставлять его в ChatGPT/Codex;
- не сохранять cookies в коде.

### 2. Сохранить HTML

К рабочей cURL-команде добавить:

```
--output hotel_<hotel_id>.html
```

Например:

```
--output hotel_1418.html
```

Проверенный результат:
- файл успешно скачан;
- размер тестовой карточки ~419 KB.

## Комментарии менеджеров

В HTML есть блок:

```html
<h4>Комментарии менеджеров</h4>
```

Таблица:

```html
<table class="table table-hover manager-comments-table">
```

Колонки:
- Автор
- Дата
- Комментарий
- Детальный

## Проверенный пример данных hotel_id=1418

Были извлечены 4 комментария менеджеров.

Пример полей:

```
AUTHOR: Анарбеков А.У.
DATE: 28.10.2024
DETAILED: нет
COMMENT: ...
```

В комментариях встречаются полезные факты:
- год открытия;
- депозит;
- бассейны;
- детская комната;
- спортзал;
- тапочки / халаты;
- сейф;
- shuttle bus;
- extra bed;
- питание;
- расстояние до моря;
- запахи / состояние номеров;
- рекомендации по целевой аудитории.

## Проверенный парсинг comments table

Локально уже отработал Python-парсер на regex + HTML cleanup.

Идея:

```python
table_match = re.search(
    r'<table class="table table-hover manager-comments-table">(.*?)</table>',
    html,
    re.S
)

rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.S)

cells = re.findall(r'<td.*?>(.*?)</td>', row, re.S)
```

После очистки HTML результат нормализуется в:

```json
{
  "author": "...",
  "date": "...",
  "comment": "...",
  "detailed": "..."
}
```

Для production-кода предпочтительнее использовать HTML parser (например BeautifulSoup/lxml), а не regex, если dependency-policy позволяет.

## Что хранить в системе

### Raw source

```
hotel_id
source_url
fetched_at
raw_manager_comments[]
```

Для каждого комментария:

```
author
date
comment
detailed
```

### Extracted hotel features

Отдельным слоем извлекать структурированные признаки из комментариев:

```
opening_year
renovation_year
deposit
beach_walk_minutes
wifi
shuttle_bus
gym
safe
bathrobes
slippers
extra_bed
meal_options
all_inclusive
room_smell_issue
location_lively
youth_friendly
family_friendly
room_quality_notes
cleanliness_notes
service_notes
audience_notes
```

Нельзя заменять raw comments только тегами — источник должен сохраняться.

## Как использовать в Travel Assistant

Признаки из DVHT нужны для персонализации выдачи отелей.

Примеры:
- высокий `cleanliness_importance` → понижать отель с повторяющимися жалобами на запахи/грязь;
- высокий `quiet_importance` → понижать отель на оживлённой улице;
- высокий `nightlife_interest` → повышать отель рядом с Bangla Road / Hard Rock;
- высокий `hotel_comfort_importance` → учитывать возраст номерного фонда и room quality;
- budget-first пользователь → допускать более слабый comfort fit при сильной цене/локации.

## Production integration

НЕ использовать личные cookies пользователя в production.

Приоритет интеграции:
1. официальный/internal API + service token;
2. service account + поддерживаемый login flow;
3. headless/session-based scraper только если внутреннего API нет и это согласовано.

Если будет service account:
- session должна жить серверно;
- cookies хранить только в secret storage;
- предусмотреть re-login;
- логировать auth failures;
- не коммитить cookies;
- не возвращать cookies в frontend.

## Безопасность

Запрещено коммитить:
- `PHPSESSID`;
- Cookie header;
- Copy-as-cURL из браузера;
- пароли DVHT;
- service tokens;
- личные browser session values.

## Текущая неопределённость

Пока не выяснено:
- есть ли официальный внутренний API для hotel card;
- есть ли service token;
- есть ли service account;
- как долго живёт browser session;
- есть ли rate limits;
- разрешён ли production scraping этой админки.

Codex не должен предполагать ответы на эти вопросы.
Нужно либо спросить пользователя, либо исследовать доступную документацию/инфраструктуру.
