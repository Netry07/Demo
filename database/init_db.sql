-- =========================================================
-- Схема базы данных "shop" для приложения "Магазин обуви"
-- Составлено на основе анализа database/queries.py
-- и import_from_excel.py
-- =========================================================

-- Таблица пользователей (роли: Администратор, Менеджер;
-- незарегистрированный вход в приложении обрабатывается как "Гость" на уровне кода)
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    role        VARCHAR(50)  NOT NULL,
    full_name   VARCHAR(150) NOT NULL,
    login       VARCHAR(150) NOT NULL UNIQUE,
    password    VARCHAR(150) NOT NULL
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS products (
    id                  SERIAL PRIMARY KEY,
    article             VARCHAR(20)     NOT NULL UNIQUE,
    name                VARCHAR(200)    NOT NULL,
    unit_of_measurement VARCHAR(20)     NOT NULL DEFAULT 'шт',
    price               NUMERIC(10, 2)  NOT NULL DEFAULT 0,
    provider            VARCHAR(150),
    category            VARCHAR(100),
    discount            SMALLINT        NOT NULL DEFAULT 0 CHECK (discount BETWEEN 0 AND 100),
    count               INTEGER         NOT NULL DEFAULT 0,
    description         TEXT,
    image               VARCHAR(255)
);

-- Таблица пунктов выдачи
CREATE TABLE IF NOT EXISTS pickup_points (
    id           INTEGER PRIMARY KEY,
    full_address VARCHAR(255) NOT NULL
);

-- Таблица заказов (имя "order" зарезервировано в SQL, поэтому в кавычках)
CREATE TABLE IF NOT EXISTS "order" (
    id              SERIAL PRIMARY KEY,
    article         VARCHAR(255) NOT NULL,
    user_id         INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    pick_up_id      INTEGER      NOT NULL REFERENCES pickup_points(id),
    created_at      DATE         NOT NULL,
    delivered_at    DATE,
    full_name       VARCHAR(150) NOT NULL,
    recipient_code  VARCHAR(20),
    status          VARCHAR(50)  NOT NULL DEFAULT 'Новый'
);

-- Таблица позиций заказа (используется для подсчёта суммы и проверки перед удалением товара)
CREATE TABLE IF NOT EXISTS order_items (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER        NOT NULL REFERENCES "order"(id) ON DELETE CASCADE,
    goods_id    INTEGER        NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER        NOT NULL DEFAULT 1,
    total_price NUMERIC(10, 2) NOT NULL DEFAULT 0
);

-- Индексы для ускорения поиска/фильтрации
CREATE INDEX IF NOT EXISTS idx_products_provider ON products(provider);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_order_status ON "order"(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
