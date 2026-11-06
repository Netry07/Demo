"""Настройки приложения. Параметры подключения к БД читаются из config.ini."""
import configparser
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

_parser = configparser.ConfigParser(interpolation=None)
if not _parser.read(CONFIG_FILE, encoding='utf-8'):
    raise FileNotFoundError(
        f'Не найден файл настроек {CONFIG_FILE}. '
        'Скопируйте config.ini.example в config.ini и укажите параметры подключения к БД.'
    )

_db = _parser['database']
DB_CONFIG = {
    'host': _db['host'],
    'port': _db.getint('port'),
    'database': _db['name'],
    'user': _db['user'],
    'password': _db['password'],
}

# Необязательные данные для автозаполнения формы входа (раздел [dev])
DEV_CONFIG = {
    'login': _parser.get('dev', 'login', fallback=''),
    'password': _parser.get('dev', 'password', fallback=''),
}

APP_CONFIG = {
    'app_name': 'Магазин обуви',
    'window_width': 1200,
    'window_height': 800,
    'image_max_width': 300,
    'image_max_height': 200,
}

# Цвета для подсветки товаров
COLORS = {
    'discount_high': '#2E8B57',    # Зеленый для скидки > 15%
    'out_of_stock': '#87CEEB',     # Голубой для товаров не в наличии
    'price_original': '#FF0000',   # Красный для зачеркнутой цены
    'price_discount': '#000000',   # Черный для цены со скидкой
}

RESOURCES = {
    'products_folder': 'resources/products/',
    'placeholder_image': 'resources/images/picture.png',
    'logo': 'resources/images/icon.ico',
}
