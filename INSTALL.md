# Установка и запуск ShoeStore

Приложение «Магазин обуви» (Python, PyQt6) поставляется как готовая сборка PyInstaller (режим onedir) для Linux. База данных PostgreSQL **не входит** в исполняемый файл: она запускается отдельно через Docker Compose.

## Требования

- Linux (сборка выполнена на CachyOS, x86_64)
- Docker и Docker Compose (`docker compose version`)
- Свободный порт 5433 на 127.0.0.1

## Состав комплекта

```
ShoeStore-release/
├── application/ShoeStore/     сборка (исполняемый файл ShoeStore и каталог _internal)
├── deployment/
│   ├── compose.yaml
│   ├── .env.example
│   ├── database/shoe_store.sql
│   └── docker/db-check/       сервис диагностики подключения
├── config.ini.example
├── README.md
└── INSTALL.md
```

## 1. Подготовка базы данных

```fish
cd deployment
cp .env.example .env
```

Откройте `.env` и укажите локальный пароль (не публикуйте его и не добавляйте в архив).
Значения базы и пользователя должны совпадать с примером: `shoe_store` и `shoe_user`.

```fish
docker compose up -d
docker compose ps
```

Сервис `db` должен перейти в состояние `healthy`.
Том с данными называется `<имя_каталога>_db_data` (для каталога `deployment` это `deployment_db_data`).

## 2. Первичный импорт данных (только при новой пустой базе)

```fish
docker compose cp database/shoe_store.sql db:/tmp/shoe_store.sql
docker compose exec db psql -v ON_ERROR_STOP=1 -U shoe_user -d shoe_store -f /tmp/shoe_store.sql
```

Если база уже содержит данные, повторный импорт без проверки не выполняйте.
Проверка: `docker compose run --rm db-check` должен вывести `OK` и число таблиц (5).

## 3. Настройка приложения

```fish
cd ..
cp config.ini.example application/ShoeStore/config.ini
```

Файл `config.ini` должен лежать **рядом с исполняемым файлом** `ShoeStore`.
В нём укажите:

```ini
[database]
host = 127.0.0.1
port = 5433
name = shoe_store
user = shoe_user
password = ВАШ_ЛОКАЛЬНЫЙ_ПАРОЛЬ
```

Пароль должен совпадать с `POSTGRES_PASSWORD` из `deployment/.env`.

## 4. Запуск

```fish
./application/ShoeStore/ShoeStore
```

Каталог `_internal` рядом с исполняемым файлом нужен для работы: переносить один файл отдельно нельзя.

## 5. Проверка

Откроется окно авторизации. После входа должен загрузиться каталог товаров с изображениями и данными из базы.

## 6. Остановка

```fish
cd deployment
docker compose stop
```

**Не используйте `docker compose down -v`**: команда удаляет том и все данные базы. Перед такими действиями делайте резервную копию (`pg_dump`).

## Типичные проблемы

| Симптом | Причина | Действия |
|---|---|---|
| `Не найден файл настроек … config.ini` | `config.ini` лежит не рядом с `ShoeStore` | Скопировать `config.ini.example` в `application/ShoeStore/config.ini` |
| Окно открылось, но данных нет или ошибка подключения | БД остановлена, неверный порт или пароль | `docker compose ps`, проверить `127.0.0.1:5433` и пароль в `config.ini` |
| `permission denied` при запуске | Нет бита исполнения | `chmod +x application/ShoeStore/ShoeStore` |
| Нет изображений | Перенесён не весь каталог | Копировать каталог `ShoeStore` целиком вместе с `_internal` |
| `docker compose up` не собирает `db-check` | Нет каталога `deployment/docker/db-check` | Использовать комплект целиком |

## Диагностика подключения

```fish
cd deployment
docker compose run --rm db-check
```

Секреты (`.env`, `config.ini` с паролем) в архив не включаются.
