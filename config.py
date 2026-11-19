import configparser
import os
import sys

# Каталог упакованных ресурсов: в обычном режиме это каталог проекта,
# в сборке PyInstaller (onedir) модуль лежит в _internal, куда копируются ресурсы.
BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    """Абсолютный путь к ресурсу, заданному относительно корня проекта (resources/...)."""
    return os.path.join(BUNDLE_DIR, *relative_path.split('/'))
# Каталог внешней конфигурации: рядом с исполняемым файлом в сборке
# и рядом с config.py при запуске из исходников.
if getattr(sys, 'frozen', False):
    EXTERNAL_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    EXTERNAL_DIR = BUNDLE_DIR

CONFIG_FILE = os.path.join(EXTERNAL_DIR, 'config.ini')

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
    'products_folder': os.path.join(BUNDLE_DIR, 'resources', 'products', ''),
    'placeholder_image': os.path.join(BUNDLE_DIR, 'resources', 'images', 'picture.png'),
    'logo': os.path.join(BUNDLE_DIR, 'resources', 'images', 'icon.ico'),
}
