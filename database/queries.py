from database.connection import db


class UserQueries:

    @staticmethod
    def authenticate(login, password):
        """Аутентификация пользователя"""
        query = """
            SELECT id as user_id, full_name, login, role as role_name
            FROM users
            WHERE login = %s AND password = %s
        """
        return db.execute_one(query, (login, password))

    @staticmethod
    def get_all_users():
        """Получить всех пользователей"""
        query = """
            SELECT id as user_id, role as role_name, full_name, login
            FROM users
            ORDER BY full_name
        """
        return db.execute_query(query)


class ProductQueries:

    @staticmethod
    def get_all_products():
        """Получить все товары с полной информацией"""
        query = """
            SELECT
                id as product_id,
                article,
                name as product_name,
                price,
                discount as current_discount,
                count as quantity_in_stock,
                description,
                image as photo_path,
                unit_of_measurement as unit_name,
                category as category_name,
                provider as supplier_name,
                ROUND(price * (1 - discount / 100.0), 2) as price_with_discount
            FROM products
            ORDER BY name
        """
        return db.execute_query(query)

    @staticmethod
    def search_products(search_text):
        """Поиск товаров по тексту"""
        query = """
            SELECT
                id as product_id,
                article,
                name as product_name,
                price,
                discount as current_discount,
                count as quantity_in_stock,
                description,
                image as photo_path,
                unit_of_measurement as unit_name,
                category as category_name,
                provider as supplier_name,
                ROUND(price * (1 - discount / 100.0), 2) as price_with_discount
            FROM products
            WHERE
                LOWER(name) LIKE LOWER(%s) OR
                LOWER(article) LIKE LOWER(%s) OR
                LOWER(COALESCE(description, '')) LIKE LOWER(%s) OR
                LOWER(COALESCE(provider, '')) LIKE LOWER(%s) OR
                LOWER(COALESCE(category, '')) LIKE LOWER(%s)
            ORDER BY name
        """
        search_pattern = f'%{search_text}%'
        return db.execute_query(query, (search_pattern,) * 5)

    @staticmethod
    def filter_by_supplier(supplier_name):
        """Фильтр товаров по поставщику"""
        query = """
            SELECT
                id as product_id,
                article,
                name as product_name,
                price,
                discount as current_discount,
                count as quantity_in_stock,
                description,
                image as photo_path,
                unit_of_measurement as unit_name,
                category as category_name,
                provider as supplier_name,
                ROUND(price * (1 - discount / 100.0), 2) as price_with_discount
            FROM products
            WHERE provider = %s
            ORDER BY name
        """
        return db.execute_query(query, (supplier_name,))

    @staticmethod
    def get_product_by_id(product_id):
        """Получить товар по ID"""
        query = """
            SELECT
                id as product_id,
                article,
                name as product_name,
                unit_of_measurement as unit_name,
                price,
                provider as supplier_name,
                category as category_name,
                discount as current_discount,
                count as quantity_in_stock,
                description,
                image as photo_path
            FROM products
            WHERE id = %s
        """
        return db.execute_one(query, (product_id,))

    @staticmethod
    def add_product(article, name, unit, price, supplier, category,
                   discount, quantity, description, photo_path):
        """Добавить новый товар"""
        query = """
            INSERT INTO products
            (article, name, unit_of_measurement, price, provider, category,
             discount, count, description, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = db.execute_one(query, (article, name, unit, price, supplier,
                                       category, discount, quantity, description, photo_path))
        return result['id'] if result else None

    @staticmethod
    def update_product(product_id, article, name, unit, price, supplier,
                      category, discount, quantity, description, photo_path):
        """Обновить товар"""
        query = """
            UPDATE products SET
                article = %s,
                name = %s,
                unit_of_measurement = %s,
                price = %s,
                provider = %s,
                category = %s,
                discount = %s,
                count = %s,
                description = %s,
                image = %s
            WHERE id = %s
        """
        return db.execute_query(query, (article, name, unit, price, supplier,
                                       category, discount, quantity, description,
                                       photo_path, product_id),
                               fetch=False)

    @staticmethod
    def delete_product(product_id):
        """Удалить товар"""
        # Проверяем, есть ли товар в заказах
        check_query = """
            SELECT COUNT(*) as count FROM order_items WHERE goods_id = %s
        """
        result = db.execute_one(check_query, (product_id,))

        if result and result['count'] > 0:
            raise Exception("Невозможно удалить товар, который присутствует в заказах")

        query = "DELETE FROM products WHERE id = %s"
        return db.execute_query(query, (product_id,), fetch=False)

    @staticmethod
    def get_all_suppliers():
        """Получить всех уникальных поставщиков"""
        query = """
            SELECT DISTINCT provider as supplier_name
            FROM products
            WHERE provider IS NOT NULL
            ORDER BY provider
        """
        return db.execute_query(query)

    @staticmethod
    def get_all_categories():
        """Получить все уникальные категории"""
        query = """
            SELECT DISTINCT category as category_name
            FROM products
            WHERE category IS NOT NULL
            ORDER BY category
        """
        return db.execute_query(query)

    @staticmethod
    def get_all_units():
        """Получить все уникальные единицы измерения"""
        query = """
            SELECT DISTINCT unit_of_measurement as unit_name
            FROM products
            WHERE unit_of_measurement IS NOT NULL
            ORDER BY unit_of_measurement
        """
        return db.execute_query(query)


class OrderQueries:
    """SQL запросы для работы с заказами"""

    @staticmethod
    def get_all_orders():
        """Получить все заказы"""
        query = """
            SELECT
                o.id as order_id,
                o.recipient_code,
                o.created_at as order_date,
                o.delivered_at as delivery_date,
                pp.full_address as pickup_address,
                o.full_name as client_name,
                o.status as status_name,
                u.login as user_login,
                COUNT(oi.goods_id) as items_count,
                SUM(oi.total_price) as total_amount
            FROM "order" o
            JOIN pickup_points pp ON o.pick_up_id = pp.id
            JOIN users u ON o.user_id = u.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id, pp.full_address, u.login
            ORDER BY o.created_at DESC
        """
        return db.execute_query(query)

    @staticmethod
    def get_order_by_id(order_id):
        """Получить заказ по ID"""
        query = """
            SELECT
                o.id as order_id,
                o.user_id,
                o.pick_up_id as pickup_point_id,
                o.created_at as order_date,
                o.delivered_at as delivery_date,
                o.full_name as client_name,
                o.recipient_code,
                o.status as status_name,
                pp.full_address
            FROM "order" o
            JOIN pickup_points pp ON o.pick_up_id = pp.id
            WHERE o.id = %s
        """
        return db.execute_one(query, (order_id,))

    @staticmethod
    def add_order(user_id, pickup_point_id, created_at, delivered_at,
                 client_name, recipient_code, status):
        """Добавить новый заказ"""
        query = """
            INSERT INTO "order"
            (user_id, pick_up_id, created_at, delivered_at, full_name, recipient_code, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = db.execute_one(query, (user_id, pickup_point_id, created_at, delivered_at,
                                       client_name, recipient_code, status))
        return result['id'] if result else None

    @staticmethod
    def update_order(order_id, pickup_point_id, created_at, delivered_at,
                    client_name, recipient_code, status):
        """Обновить заказ"""
        query = """
            UPDATE "order" SET
                pick_up_id = %s,
                created_at = %s,
                delivered_at = %s,
                full_name = %s,
                recipient_code = %s,
                status = %s
            WHERE id = %s
        """
        return db.execute_query(query, (pickup_point_id, created_at, delivered_at,
                                       client_name, recipient_code, status, order_id),
                               fetch=False)

    @staticmethod
    def delete_order(order_id):
        """Удалить заказ (каскадное удаление order_items)"""
        query = 'DELETE FROM "order" WHERE id = %s'
        return db.execute_query(query, (order_id,), fetch=False)

    @staticmethod
    def get_all_pickup_points():
        """Получить все пункты выдачи"""
        query = "SELECT id as point_id, full_address FROM pickup_points ORDER BY full_address"
        return db.execute_query(query)

    @staticmethod
    def get_all_statuses():
        """Получить все уникальные статусы заказов"""
        query = """
            SELECT DISTINCT status as status_name
            FROM "order"
            ORDER BY status
        """
        return db.execute_query(query)
