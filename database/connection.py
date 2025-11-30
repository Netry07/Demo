import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


class DatabaseConnection:
    """Класс для управления подключением к базе данных PostgreSQL"""

    _instance = None
    _connection = None

    def __new__(cls):
        """Singleton паттерн - одно подключение на все приложение"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        """Установить подключение к базе данных"""
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=DB_CONFIG['host'],
                    port=DB_CONFIG['port'],
                    database=DB_CONFIG['database'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    cursor_factory=RealDictCursor
                )
                print("Подключение к базе данных установлено")
            return self._connection
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def disconnect(self):
        """Закрыть подключение к базе данных"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            print("Подключение к базе данных закрыто")

    def execute_query(self, query, params=None, fetch=True):
        """
        Выполнить SQL запрос

        Args:
            query: SQL запрос
            params: Параметры запроса (tuple)
            fetch: Возвращать ли результат (True для SELECT)

        Returns:
            Результат запроса или None
        """
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)

                if fetch:
                    result = cursor.fetchall()
                    return result
                else:
                    conn.commit()
                    return cursor.rowcount

        except Exception as e:
            if self._connection:
                self._connection.rollback()
            print(f"Ошибка выполнения запроса: {e}")
            raise

    def execute_one(self, query, params=None):
        """
        Выполнить запрос и вернуть одну строку

        Args:
            query: SQL запрос
            params: Параметры запроса

        Returns:
            Одна строка результата или None
        """
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            raise


# Создаем глобальный экземпляр подключения
db = DatabaseConnection()
