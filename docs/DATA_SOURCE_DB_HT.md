# Internal hotel data source — db.ht.kz

## Что проверено

Карточка отеля доступна по точному ID:

https://db.ht.kz/tours/hotel/update/id/{hotel_id}

Пример:
hotel_id = 1418

Страница возвращает серверный HTML.
Основные данные и комментарии менеджеров находятся прямо внутри HTML, а не в отдельном JSON endpoint.

## Проверенный способ

В авторизованном браузере:
1. DevTools → Network.
2. Выбрать основной Doc-запрос.
3. Copy → Copy as cURL.
4. Выполнить cURL локально.
5. Ответ можно сохранить в HTML-файл.

Это подтвердило, что авторизованная сессия может получить полный HTML карточки.

## Авторизация

db.ht.kz на проверенной странице использует cookie-based session.
В Request Headers присутствуют cookies, включая PHPSESSID.

Bearer-token для этой страницы не обнаружен.

## Важное ограничение

Не использовать личные browser cookies как production-интеграцию.

Предпочтительный порядок:
1. внутренний API / service token;
2. отдельный service account + устойчивый механизм логина;
3. только для локального исследования — Copy as cURL из браузера.

## Manager comments

В HTML найден блок:

<h4>Комментарии менеджеров</h4>

Таблица:
table.manager-comments-table

Колонки:
- Автор
- Дата
- Комментарий
- Детальный

Пример данных из hotel_id=1418 включал:
- год открытия;
- депозит;
- бассейн;
- наличие детской комнаты;
- спортзал;
- сейф;
- extra bed;
- питание;
- расстояние до моря;
- замечания по номерам;
- рекомендации по целевой аудитории.

## Что можно извлекать

Планируемые нормализованные поля:
- hotel_id
- name
- stars
- manager_comments[]
  - author
  - date
  - comment
  - detailed
- photos[]
- room_notes
- beach_notes
- food_notes
- distance_to_sea
- opening_year
- renovation_year
- cleanliness_notes
- service_notes
- audience_notes

## Потенциал для Travel Assistant

Комментарии менеджеров могут стать источником качественных признаков:
- quiet
- good_for_youth
- family_friendly
- old_rooms
- good_food
- far_from_sea
- cleanliness_issue
- service_issue
- strong_location
- weak_location

LLM может извлекать теги, но исходный комментарий и источник должны сохраняться.
