# Магазин обуви — система учёта товаров и заказов

Учебный проект: десктопное приложение (PyQt6 + PostgreSQL) для ведения каталога
обуви и оформления заказов с разграничением прав доступа.

## Возможности

- просмотр каталога обуви с ценой, скидкой и количеством на складе;
- поиск, фильтрация и сортировка товаров;
- вход под ролями: гость, клиент, менеджер, администратор;
- добавление, редактирование и удаление товаров (администратор);
- оформление заказов и управление ими (менеджер и администратор).

## Требования

- Python 3.10 и выше
- PostgreSQL 14 и выше
- библиотеки из файла `requirements.txt`

## Установка и запуск

1. Клонировать репозиторий: `git clone git@github.com:Netry07/Demo.git && cd Demo`
2. Создать окружение и установить зависимости:
   `python -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
3. Создать базу данных и загрузить скрипт с данными:
   `createdb shop`, `psql -d shop -f database/shoe_store.sql`
4. Скопировать `config.ini.example` в `config.ini` и указать параметры подключения к БД.
5. Запустить приложение: `python main.py`

Первичный импорт из Excel (`import_from_excel.py`) нужен только при пустой базе;
для него дополнительно требуются `pandas` и `openpyxl`.

## Структура репозитория

- `main.py` — точка входа
- `config.py` — чтение настроек из `config.ini`
- `views/` — окна и диалоги приложения
- `database/` — подключение к БД, запросы, схема `init_db.sql` и скрипт с данными `shoe_store.sql`
- `resources/` — изображения, иконка, фотографии товаров
- `excel_data/` — исходные данные для импорта
- `docs/` — ER-диаграмма

## ER-диаграмма базы данных

Диаграмма находится в файле `docs/er_diagram.pdf` (исходник для Graphviz — `docs/er_diagram.dot`).
Основные таблицы:

- `users` — пользователи и их роли;
- `products` — каталог товаров;
- `pickup_points` — пункты выдачи;
- `order` — заказы (связаны с `users` и `pickup_points`);
- `order_items` — позиции заказов (связывают `order` и `products`).

## Запуск PostgreSQL через Docker Compose

### Требования
Docker Engine и плагин Docker Compose v2 (`docker --version`, `docker compose version`).

### Подготовка
1. Скопировать шаблон: `cp .env.example .env`
2. В `.env` указать собственный локальный пароль в `POSTGRES_PASSWORD`. Файл `.env` в Git не добавляется.

### Запуск

docker compose up --build -d
docker compose ps -a
docker compose logs --tail=40 db-check

Сервис `db` должен быть в состоянии healthy, `db-check` завершается с кодом 0 (одноразовая проверка).

### Импорт базы данных

docker compose cp database/shoe_store.sql db:/tmp/shoe_store.sql
docker compose exec db psql -v ON_ERROR_STOP=1 -U shoe_user -d shoe_store -f /tmp/shoe_store.sql
docker compose run --rm db-check

### Подключение приложения
В локальном `config.ini` (в Git не добавляется): `host = localhost`, `port = 5433`, `name = shoe_store`, `user = shoe_user`, пароль из `.env`.
Внутри Compose сервис `db-check` подключается к `db:5432`.

### Проверка и остановка

docker compose exec db pg_isready -U shoe_user -d shoe_store
docker compose stop
docker compose start

Команду `docker compose down -v` не использовать: она удаляет данные.
