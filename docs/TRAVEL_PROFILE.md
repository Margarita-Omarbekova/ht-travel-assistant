# Travel Profile v1

Travel Profile — структурированное представление потребностей пользователя.
Он собирается постепенно из свободного диалога, а не анкетой.

## Hard constraints

- citizenship
- departure_city
- travel_dates
- date_flexibility
- duration
- adults
- children
- children_ages
- budget
- currency
- max_travel_time
- direct_flight_required
- max_connections
- visa_tolerance

## Climate & environment

- heat_tolerance
- humidity_tolerance
- wind_preference
- rain_tolerance
- sea_temperature_preference
- crowd_tolerance
- cleanliness_importance
- safety_importance
- noise_tolerance
- walkability_importance
- infrastructure_importance

## Hotel preferences

- hotel_as_experience
- hotel_comfort_importance
- cleanliness_importance
- room_quality_importance
- bed_quality_importance
- service_importance
- food_importance
- all_inclusive_interest
- design_aesthetic_importance
- instagrammable_interest
- boutique_interest
- resort_interest
- room_only_ok

## Travel style

- beach_interest
- sightseeing_interest
- nature_interest
- nightlife_interest
- gastronomy_interest
- shopping_interest
- spa_interest
- adventure_interest
- excursion_interest
- self_guided_interest
- car_rental_tolerance
- daily_activity_level
- early_wakeup_tolerance
- hotel_change_tolerance
- internal_transfer_tolerance

## Anti-preferences

Хранить отдельно, потому что они могут быть сильнее позитивных предпочтений.

Примеры:
- no_crowds
- no_all_inclusive
- no_long_transfer
- no_dirty_environment
- no_nightlife
- no_complex_visa
- no_children_environment
- no_heat
- no_car_rental
- excluded_countries

## Dream / visual layer

Пользователь может:
- описать идеальный день;
- прислать фото;
- прислать визуальные референсы;
- выбрать примеры.

LLM превращает это в теги, например:
- sea_view
- moody_weather
- quiet
- few_people
- boutique_hotel
- cliffs
- old_town
- good_food
- slow_travel
- luxury
- wild_beach

## UX principle

Не задавать абстрактные вопросы без подсказок.

Вместо:
“Насколько важен отель?”

Предлагать примеры:
- только переночевать;
- главное чисто и удобно;
- атмосферный отель как часть отдыха;
- вау-эффект: виды, интерьер, бассейн;
- свой вариант.

Допускать несколько ответов одновременно.
