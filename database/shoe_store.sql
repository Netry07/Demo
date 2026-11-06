--
-- PostgreSQL database dump
--


-- Dumped from database version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."order" (
    id integer NOT NULL,
    article character varying(255) NOT NULL,
    user_id integer,
    pick_up_id integer NOT NULL,
    created_at date NOT NULL,
    delivered_at date,
    full_name character varying(150) NOT NULL,
    recipient_code character varying(20),
    status character varying(50) DEFAULT 'Новый'::character varying NOT NULL
);


--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_id_seq OWNED BY public."order".id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    goods_id integer NOT NULL,
    quantity integer DEFAULT 1 NOT NULL,
    total_price numeric(10,2) DEFAULT 0 NOT NULL
);


--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: pickup_points; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pickup_points (
    id integer NOT NULL,
    full_address character varying(255) NOT NULL
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    article character varying(20) NOT NULL,
    name character varying(200) NOT NULL,
    unit_of_measurement character varying(20) DEFAULT 'шт'::character varying NOT NULL,
    price numeric(10,2) DEFAULT 0 NOT NULL,
    provider character varying(150),
    category character varying(100),
    discount smallint DEFAULT 0 NOT NULL,
    count integer DEFAULT 0 NOT NULL,
    description text,
    image character varying(255),
    CONSTRAINT products_discount_check CHECK (((discount >= 0) AND (discount <= 100)))
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    role character varying(50) NOT NULL,
    full_name character varying(150) NOT NULL,
    login character varying(150) NOT NULL,
    password character varying(150) NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: order id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order" ALTER COLUMN id SET DEFAULT nextval('public.order_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (1, 'А112Т4, 2, F635R4, 2', 4, 1, '2025-02-27', '2025-04-20', 'Степанов Михаил Артёмович', '901', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (2, 'H782T5, 1, G783F5, 1', 1, 11, '2022-09-28', '2025-04-21', 'Никифорова Весения Николаевна', '902', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (3, 'J384T6, 10, D572U8, 10', 2, 2, '2025-03-21', '2025-04-22', 'Сазонов Руслан Германович', '903', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (4, 'F572H7, 5, D329H3, 4', 3, 11, '2025-02-20', '2025-04-23', 'Одинцов Серафим Артёмович', '904', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (5, 'А112Т4, 2, F635R4, 2', 4, 2, '2025-03-17', '2025-04-24', 'Степанов Михаил Артёмович', '905', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (6, 'H782T5, 1, G783F5, 1', 1, 15, '2025-03-01', '2025-04-25', 'Никифорова Весения Николаевна', '906', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (7, 'J384T6, 10, D572U8, 10', 2, 3, '2025-02-28', '2025-04-26', 'Сазонов Руслан Германович', '907', 'Завершен');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (8, 'F572H7, 5, D329H3, 4', 3, 19, '2025-03-31', '2025-04-27', 'Одинцов Серафим Артёмович', '908', 'Новый ');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (9, 'B320R5, 5, G432E4, 1', 4, 5, '2025-04-02', '2025-04-28', 'Степанов Михаил Артёмович', '909', 'Новый ');
INSERT INTO public."order" (id, article, user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status) VALUES (10, 'S213E3, 5, E482R4, 5', 4, 19, '2025-04-03', '2025-04-29', 'Степанов Михаил Артёмович', '910', 'Новый ');


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: pickup_points; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.pickup_points (id, full_address) VALUES (0, '420151, г. Лесной, ул. Вишневая, 32');
INSERT INTO public.pickup_points (id, full_address) VALUES (1, '125061, г. Лесной, ул. Подгорная, 8');
INSERT INTO public.pickup_points (id, full_address) VALUES (2, '630370, г. Лесной, ул. Шоссейная, 24');
INSERT INTO public.pickup_points (id, full_address) VALUES (3, '400562, г. Лесной, ул. Зеленая, 32');
INSERT INTO public.pickup_points (id, full_address) VALUES (4, '614510, г. Лесной, ул. Маяковского, 47');
INSERT INTO public.pickup_points (id, full_address) VALUES (5, '410542, г. Лесной, ул. Светлая, 46');
INSERT INTO public.pickup_points (id, full_address) VALUES (6, '620839, г. Лесной, ул. Цветочная, 8');
INSERT INTO public.pickup_points (id, full_address) VALUES (7, '443890, г. Лесной, ул. Коммунистическая, 1');
INSERT INTO public.pickup_points (id, full_address) VALUES (8, '603379, г. Лесной, ул. Спортивная, 46');
INSERT INTO public.pickup_points (id, full_address) VALUES (9, '603721, г. Лесной, ул. Гоголя, 41');
INSERT INTO public.pickup_points (id, full_address) VALUES (10, '410172, г. Лесной, ул. Северная, 13');
INSERT INTO public.pickup_points (id, full_address) VALUES (11, '614611, г. Лесной, ул. Молодежная, 50');
INSERT INTO public.pickup_points (id, full_address) VALUES (12, '454311, г.Лесной, ул. Новая, 19');
INSERT INTO public.pickup_points (id, full_address) VALUES (13, '660007, г.Лесной, ул. Октябрьская, 19');
INSERT INTO public.pickup_points (id, full_address) VALUES (14, '603036, г. Лесной, ул. Садовая, 4');
INSERT INTO public.pickup_points (id, full_address) VALUES (15, '394060, г.Лесной, ул. Фрунзе, 43');
INSERT INTO public.pickup_points (id, full_address) VALUES (16, '410661, г. Лесной, ул. Школьная, 50');
INSERT INTO public.pickup_points (id, full_address) VALUES (17, '625590, г. Лесной, ул. Коммунистическая, 20');
INSERT INTO public.pickup_points (id, full_address) VALUES (18, '625683, г. Лесной, ул. 8 Марта');
INSERT INTO public.pickup_points (id, full_address) VALUES (19, '450983, г.Лесной, ул. Комсомольская, 26');
INSERT INTO public.pickup_points (id, full_address) VALUES (20, '394782, г. Лесной, ул. Чехова, 3');
INSERT INTO public.pickup_points (id, full_address) VALUES (21, '603002, г. Лесной, ул. Дзержинского, 28');
INSERT INTO public.pickup_points (id, full_address) VALUES (22, '450558, г. Лесной, ул. Набережная, 30');
INSERT INTO public.pickup_points (id, full_address) VALUES (23, '344288, г. Лесной, ул. Чехова, 1');
INSERT INTO public.pickup_points (id, full_address) VALUES (24, '614164, г.Лесной,  ул. Степная, 30');
INSERT INTO public.pickup_points (id, full_address) VALUES (25, '394242, г. Лесной, ул. Коммунистическая, 43');
INSERT INTO public.pickup_points (id, full_address) VALUES (26, '660540, г. Лесной, ул. Солнечная, 25');
INSERT INTO public.pickup_points (id, full_address) VALUES (27, '125837, г. Лесной, ул. Шоссейная, 40');
INSERT INTO public.pickup_points (id, full_address) VALUES (28, '125703, г. Лесной, ул. Партизанская, 49');
INSERT INTO public.pickup_points (id, full_address) VALUES (29, '625283, г. Лесной, ул. Победы, 46');
INSERT INTO public.pickup_points (id, full_address) VALUES (30, '614753, г. Лесной, ул. Полевая, 35');
INSERT INTO public.pickup_points (id, full_address) VALUES (31, '426030, г. Лесной, ул. Маяковского, 44');
INSERT INTO public.pickup_points (id, full_address) VALUES (32, '450375, г. Лесной ул. Клубная, 44');
INSERT INTO public.pickup_points (id, full_address) VALUES (33, '625560, г. Лесной, ул. Некрасова, 12');
INSERT INTO public.pickup_points (id, full_address) VALUES (34, '630201, г. Лесной, ул. Комсомольская, 17');
INSERT INTO public.pickup_points (id, full_address) VALUES (35, '190949, г. Лесной, ул. Мичурина, 26');


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (1, 'А112Т4', 'Ботинки', 'шт.', 4990.00, 'Kari', 'Женская обувь', 3, 6, 'Женские Ботинки демисезонные kari', 'resources/products/1.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (2, 'F635R4', 'Ботинки', 'шт.', 3244.00, 'Обувь для вас', 'Женская обувь', 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', 'resources/products/2.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (3, 'H782T5', 'Туфли', 'шт.', 4499.00, 'Kari', 'Мужская обувь', 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', 'resources/products/3.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (4, 'G783F5', 'Ботинки', 'шт.', 5900.00, 'Kari', 'Мужская обувь', 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', 'resources/products/4.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (5, 'J384T6', 'Ботинки', 'шт.', 3800.00, 'Обувь для вас', 'Мужская обувь', 2, 16, 'B3430/14 Полуботинки мужские Rieker', 'resources/products/5.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (6, 'D572U8', 'Кроссовки', 'шт.', 4100.00, 'Обувь для вас', 'Мужская обувь', 3, 6, '129615-4 Кроссовки мужские', 'resources/products/6.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (7, 'F572H7', 'Туфли', 'шт.', 2700.00, 'Kari', 'Женская обувь', 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', 'resources/products/7.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (8, 'D329H3', 'Полуботинки', 'шт.', 1890.00, 'Обувь для вас', 'Женская обувь', 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', 'resources/products/8.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (9, 'B320R5', 'Туфли', 'шт.', 4300.00, 'Kari', 'Женская обувь', 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', 'resources/products/9.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (10, 'G432E4', 'Туфли', 'шт.', 2800.00, 'Kari', 'Женская обувь', 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', 'resources/products/10.jpg');
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (11, 'S213E3', 'Полуботинки', 'шт.', 2156.00, 'Обувь для вас', 'Мужская обувь', 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (12, 'E482R4', 'Полуботинки', 'шт.', 1800.00, 'Kari', 'Женская обувь', 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (13, 'S634B5', 'Кеды', 'шт.', 5500.00, 'Обувь для вас', 'Мужская обувь', 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (14, 'K345R4', 'Полуботинки', 'шт.', 2100.00, 'Обувь для вас', 'Мужская обувь', 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (15, 'O754F4', 'Туфли', 'шт.', 5400.00, 'Обувь для вас', 'Женская обувь', 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (16, 'G531F4', 'Ботинки', 'шт.', 6600.00, 'Kari', 'Женская обувь', 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (17, 'J542F5', 'Тапочки', 'шт.', 500.00, 'Kari', 'Мужская обувь', 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (18, 'B431R5', 'Ботинки', 'шт.', 2700.00, 'Обувь для вас', 'Мужская обувь', 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (19, 'P764G4', 'Туфли', 'шт.', 6800.00, 'Kari', 'Женская обувь', 15, 15, 'Туфли женские, ARGO, размер 38', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (20, 'C436G5', 'Ботинки', 'шт.', 10200.00, 'Kari', 'Женская обувь', 15, 9, 'Ботинки женские, ARGO, размер 40', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (21, 'F427R5', 'Ботинки', 'шт.', 11800.00, 'Обувь для вас', 'Женская обувь', 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (22, 'N457T5', 'Полуботинки', 'шт.', 4600.00, 'Kari', 'Женская обувь', 3, 13, 'Полуботинки Ботинки черные зимние, мех', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (23, 'D364R4', 'Туфли', 'шт.', 12400.00, 'Kari', 'Женская обувь', 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (24, 'S326R5', 'Тапочки', 'шт.', 9900.00, 'Обувь для вас', 'Мужская обувь', 17, 15, 'Мужские кожаные тапочки "Профиль С.Дали" ', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (25, 'L754R4', 'Полуботинки', 'шт.', 1700.00, 'Kari', 'Женская обувь', 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (26, 'M542T5', 'Кроссовки', 'шт.', 2800.00, 'Обувь для вас', 'Мужская обувь', 18, 3, 'Кроссовки мужские TOFA', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (27, 'D268G5', 'Туфли', 'шт.', 4399.00, 'Обувь для вас', 'Женская обувь', 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (28, 'T324F5', 'Сапоги', 'шт.', 4699.00, 'Kari', 'Женская обувь', 2, 5, 'Сапоги замша Цвет: синий', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (29, 'K358H6', 'Тапочки', 'шт.', 599.00, 'Kari', 'Мужская обувь', 20, 2, 'Тапочки мужские син р.41', NULL);
INSERT INTO public.products (id, article, name, unit_of_measurement, price, provider, category, discount, count, description, image) VALUES (30, 'H535R5', 'Ботинки', 'шт.', 2300.00, 'Обувь для вас', 'Женская обувь', 2, 7, 'Женские Ботинки демисезонные', NULL);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, role, full_name, login, password) VALUES (1, 'Администратор', 'Никифорова Весения Николаевна', '94d5ous@gmail.com', 'uzWC67');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (2, 'Администратор', 'Сазонов Руслан Германович', 'uth4iz@mail.com', '2L6KZG');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (3, 'Администратор', 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (4, 'Менеджер', 'Степанов Михаил Артёмович', '1diph5e@tutanota.com', '8ntwUp');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (5, 'Менеджер', 'Ворсин Петр Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (6, 'Менеджер', 'Старикова Елена Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (7, 'Авторизированный клиент', 'Михайлюк Анна Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (8, 'Авторизированный клиент', 'Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (9, 'Авторизированный клиент', 'Ворсин Петр Евгеньевич', '1qz4kw@mail.com', 'gynQMT');
INSERT INTO public.users (id, role, full_name, login, password) VALUES (10, 'Авторизированный клиент', 'Старикова Елена Павловна', '4np6se@mail.com', 'AtnDjr');


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.order_id_seq', 1, false);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.order_items_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 30, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: pickup_points pickup_points_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pickup_points
    ADD CONSTRAINT pickup_points_pkey PRIMARY KEY (id);


--
-- Name: products products_article_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_article_key UNIQUE (article);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_order_items_order_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_order_items_order_id ON public.order_items USING btree (order_id);


--
-- Name: idx_order_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_order_status ON public."order" USING btree (status);


--
-- Name: idx_products_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_products_category ON public.products USING btree (category);


--
-- Name: idx_products_provider; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_products_provider ON public.products USING btree (provider);


--
-- Name: order_items order_items_goods_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_goods_id_fkey FOREIGN KEY (goods_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE CASCADE;


--
-- Name: order order_pick_up_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pick_up_id_fkey FOREIGN KEY (pick_up_id) REFERENCES public.pickup_points(id);


--
-- Name: order order_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--


