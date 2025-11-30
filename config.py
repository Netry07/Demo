
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'shop',
    'user': 'postgres',
    'password': '123'
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
