import pandas as pd
import psycopg2
from config import DB_CONFIG
from datetime import datetime

EXCEL_FILES = {
    'pickup_points': 'excel_data/pickup_points.xlsx',
    'products': 'excel_data/products.xlsx',
    'users': 'excel_data/users.xlsx',
    'orders': 'excel_data/orders.xlsx'
}


def connect_db():
    """Подключение к базе данных"""
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )


def import_pickup_points(file_path):
    """Импорт пунктов выдачи"""
    print(f"\nИмпорт пунктов выдачи из {file_path}...")

    try:
        # Читаем Excel (адреса в столбце A, индекс 0)
        df = pd.read_excel(file_path, header=None)

        conn = connect_db()
        cursor = conn.cursor()

        count = 0

        for index, row in df.iterrows():
            address = str(row[0]) if pd.notna(row[0]) else None

            if address and address.strip() and 'г.' in address:
                try:
                    cursor.execute(
                        "INSERT INTO pickup_points (full_address) VALUES (%s) ON CONFLICT DO NOTHING",
                        (address.strip(),)
                    )
                    count += 1
                except Exception as e:
                    print(f"  Ошибка добавления адреса '{address[:50]}...': {e}")
                    conn.rollback()
                    continue

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Импортировано пунктов выдачи: {count}")

    except Exception as e:
        print(f"Ошибка импорта пунктов выдачи: {e}")
        import traceback
        traceback.print_exc()


def import_products(file_path):
    """Импорт товаров"""
    print(f"\nИмпорт товаров из {file_path}...")

    try:
        df = pd.read_excel(file_path)

        conn = connect_db()
        cursor = conn.cursor()

        count = 0
        for index, row in df.iterrows():
            try:
                article = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
                name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ''
                unit = str(row.iloc[2]) if pd.notna(row.iloc[2]) else 'шт'
                price = float(row.iloc[3]) if pd.notna(row.iloc[3]) else 0
                provider = str(row.iloc[4]) if pd.notna(row.iloc[4]) else ''
                category = str(row.iloc[6]) if pd.notna(row.iloc[6]) else ''
                discount = int(row.iloc[7]) if pd.notna(row.iloc[7]) else 0
                count_stock = int(row.iloc[8]) if pd.notna(row.iloc[8]) else 0
                description = str(row.iloc[9]) if pd.notna(row.iloc[9]) else ''
                image = str(row.iloc[10]) if pd.notna(row.iloc[10]) else ''
                if image and image != 'nan' and not image.startswith('resources/'):
                    image = f'resources/products/{image}'
                elif image == 'nan' or not image:
                    image = None

                cursor.execute(
                    """
                    INSERT INTO products
                    (article, name, unit_of_measurement, price, provider, category,
                     discount, count, description, image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (article) DO UPDATE SET
                        name = EXCLUDED.name,
                        price = EXCLUDED.price,
                        count = EXCLUDED.count,
                        discount = EXCLUDED.discount
                    """,
                    (article, name, unit, price, provider, category,
                     discount, count_stock, description, image)
                )
                count += 1
            except Exception as e:
                print(f"  Ошибка импорта товара строка {index + 2}: {e}")
                conn.rollback()
                continue

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Импортировано товаров: {count}")

    except Exception as e:
        print(f"Ошибка импорта товаров: {e}")


def import_users(file_path):
    """Импорт пользователей"""
    print(f"\nИмпорт пользователей из {file_path}...")

    try:
        df = pd.read_excel(file_path)

        conn = connect_db()
        cursor = conn.cursor()

        count = 0
        for index, row in df.iterrows():
            try:
                role = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
                full_name = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ''
                login = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ''
                password = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ''

                if not login or not full_name:
                    continue

                cursor.execute(
                    """
                    INSERT INTO users (role, full_name, login, password)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (login) DO UPDATE SET
                        full_name = EXCLUDED.full_name,
                        role = EXCLUDED.role,
                        password = EXCLUDED.password
                    """,
                    (role, full_name, login, password)
                )
                count += 1
            except Exception as e:
                print(f"  Ошибка импорта пользователя строка {index + 2}: {e}")
                conn.rollback()
                continue

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Импортировано пользователей: {count}")

    except Exception as e:
        print(f"Ошибка импорта пользователей: {e}")


def parse_date(date_value):
    if pd.isna(date_value):
        return None

    try:
        if isinstance(date_value, pd.Timestamp):
            return date_value.strftime('%Y-%m-%d')

        date_str = str(date_value)

        if '.' in date_str:
            parts = date_str.split('.')
            if len(parts) == 3:
                day, month, year = parts
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        dt = pd.to_datetime(date_value, dayfirst=True)
        return dt.strftime('%Y-%m-%d')

    except Exception as e:
        print(f"Ошибка парсинга даты '{date_value}': {e}")
        return None


def import_orders(file_path):
    """Импорт заказов"""
    print(f"\nИмпорт заказов из {file_path}...")

    try:
        df = pd.read_excel(file_path)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM pickup_points")
        pickup_count = cursor.fetchone()[0]

        if pickup_count == 0:
            print("  ВНИМАНИЕ: В таблице pickup_points нет записей!")
            print("  Сначала импортируйте пункты выдачи.")
            cursor.close()
            conn.close()
            return

        count = 0
        errors = 0

        for index, row in df.iterrows():
            try:
                order_number = int(row.iloc[0]) if pd.notna(row.iloc[0]) else None
                order_date = parse_date(row.iloc[2])
                delivery_date = parse_date(row.iloc[3])

                if not order_date or not delivery_date:
                    print(f"  Пропуск строки {index + 2}: некорректные даты")
                    errors += 1
                    continue

                pickup_point_id = int(row.iloc[4]) if pd.notna(row.iloc[4]) else 1

                cursor.execute("SELECT id FROM pickup_points WHERE id = %s", (pickup_point_id,))
                if not cursor.fetchone():
                    cursor.execute("SELECT id FROM pickup_points LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        pickup_point_id = result[0]
                        print(f"  Строка {index + 2}: использован пункт выдачи #{pickup_point_id}")
                    else:
                        print(f"  Пропуск строки {index + 2}: нет доступных пунктов выдачи")
                        errors += 1
                        continue

                client_name = str(row.iloc[5]) if pd.notna(row.iloc[5]) else ''

                cursor.execute("SELECT id FROM users WHERE full_name = %s LIMIT 1", (client_name,))
                user_result = cursor.fetchone()
                user_id = user_result[0] if user_result else None

                if not user_id:
                    cursor.execute("SELECT id FROM users LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        user_id = result[0]
                    else:
                        print(f"  Пропуск строки {index + 2}: нет пользователей в БД")
                        errors += 1
                        continue

                receive_code = str(int(row.iloc[6])) if pd.notna(row.iloc[6]) else ''
                status = str(row.iloc[7]) if pd.notna(row.iloc[7]) else 'Новый'

                cursor.execute(
                    """
                    INSERT INTO "order"
                    (user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (user_id, pickup_point_id, order_date, delivery_date, client_name, receive_code, status)
                )
                conn.commit()  # Коммитим каждый заказ отдельно
                count += 1

            except Exception as e:
                print(f"  Ошибка импорта заказа строка {index + 2}: {e}")
                conn.rollback()
                errors += 1
                continue

        cursor.close()
        conn.close()

        print(f"Импортировано заказов: {count}")
        if errors > 0:
            print(f"Ошибок при импорте: {errors}")

    except Exception as e:
        print(f"Ошибка импорта заказов: {e}")


def main():
    """Главная функция импорта"""
    print("=" * 60)
    print("ИМПОРТ ДАННЫХ ИЗ EXCEL В БАЗУ ДАННЫХ")
    print("=" * 60)

    # Импортируем данные в правильном порядке (с учетом внешних ключей)
    import_pickup_points(EXCEL_FILES['pickup_points'])
    import_users(EXCEL_FILES['users'])
    import_products(EXCEL_FILES['products'])
    import_orders(EXCEL_FILES['orders'])

    print("\n" + "=" * 60)
    print("ИМПОРТ ЗАВЕРШЕН!")
    print("=" * 60)


if __name__ == '__main__':
    main()
