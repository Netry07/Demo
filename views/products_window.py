import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QScrollArea, QFrame, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont
from database.queries import ProductQueries
from views.product_edit_dialog import ProductEditDialog
from views.orders_window import OrdersWindow


class ProductCard(QFrame):
    """Виджет карточки товара"""

    def __init__(self, product, user_role, parent=None):
        super().__init__(parent)
        self.product = product
        self.user_role = user_role
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """Создание интерфейса карточки"""
        layout = QVBoxLayout()
        layout.setSpacing(5)

        # Определяем фон карточки в зависимости от скидки и наличия
        if self.product['quantity_in_stock'] == 0:
            self.setObjectName('outOfStock')
            self.setStyleSheet('QFrame#outOfStock { background-color: #87CEEB; border-radius: 5px; padding: 10px; }')
        elif self.product['current_discount'] > 15:
            self.setObjectName('highDiscount')
            self.setStyleSheet('QFrame#highDiscount { background-color: #2E8B57; border-radius: 5px; padding: 10px; }')
        else:
            self.setObjectName('productCard')
            self.setStyleSheet('QFrame#productCard { background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 5px; padding: 10px; }')

        photo_label = QLabel()
        photo_label.setFixedSize(200, 150)
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_path = self.product.get('photo_path', '')
        if photo_path and os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
        else:
            pixmap = QPixmap('resources/images/picture.png')

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(scaled_pixmap)

        layout.addWidget(photo_label)

        # Название товара
        name_label = QLabel(f"<b>{self.product['product_name']}</b>")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        # Артикул
        article_label = QLabel(f"Артикул: {self.product['article']}")
        article_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(article_label)

        # Категория
        category_label = QLabel(f"Категория: {self.product['category_name']}")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(category_label)

        # Поставщик
        supplier_label = QLabel(f"Поставщик: {self.product['supplier_name']}")
        supplier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(supplier_label)

        # Цена
        price_layout = QHBoxLayout()
        price_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.product['current_discount'] > 0:
            # Зачеркнутая старая цена
            old_price_label = QLabel(f"{self.product['price']:.2f} ₽")
            old_price_label.setStyleSheet('color: #FF0000; text-decoration: line-through;')
            price_layout.addWidget(old_price_label)

            # Новая цена со скидкой
            new_price_label = QLabel(f"{self.product['price_with_discount']:.2f} ₽")
            new_price_label.setStyleSheet('color: #000000; font-weight: bold;')
            price_layout.addWidget(new_price_label)
        else:
            price_label = QLabel(f"{self.product['price']:.2f} ₽")
            price_label.setStyleSheet('font-weight: bold;')
            price_layout.addWidget(price_label)

        layout.addLayout(price_layout)

        # Скидка
        if self.product['current_discount'] > 0:
            discount_label = QLabel(f"Скидка: {self.product['current_discount']}%")
            discount_label.setStyleSheet('color: #FF0000; font-weight: bold;')
            discount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(discount_label)

        # Количество на складе
        stock_label = QLabel(f"На складе: {self.product['quantity_in_stock']} {self.product['unit_name']}")
        stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stock_label)

        # Описание (если есть)
        if self.product.get('description'):
            desc_label = QLabel(self.product['description'][:100] + '...' if len(self.product['description']) > 100 else self.product['description'])
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet('font-size: 12px; color: #666;')
            layout.addWidget(desc_label)

        self.setLayout(layout)

        if self.user_role == 'Администратор':
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.user_role == 'Администратор':
            self.parent_window.edit_product(self.product['product_id'])


class ProductsWindow(QMainWindow):
    """Главное окно со списком товаров"""

    def __init__(self, user, login_window):
        super().__init__()
        self.current_user = user
        self.login_window = login_window
        self.all_products = []
        self.filtered_products = []
        self.current_sort = None
        self.current_filter = None
        self.edit_dialog = None
        self.init_ui()
        self.load_products()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f'Список товаров - {self.current_user["full_name"]}')
        self.setMinimumSize(1200, 800)
        self.setWindowIcon(QIcon('resources/images/icon.ico'))

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Верхняя панель с информацией о пользователе
        top_panel = QHBoxLayout()

        # Логотип
        logo_label = QLabel()
        try:
            pixmap = QPixmap('resources/images/icon.ico')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                logo_label.setPixmap(scaled_pixmap)
        except:
            logo_label.setText('🏪')

        top_panel.addWidget(logo_label)
        top_panel.addStretch()

        # ФИО пользователя
        user_label = QLabel(f"{self.current_user['full_name']} ({self.current_user['role_name']})")
        user_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        top_panel.addWidget(user_label)

        # Кнопка выхода
        logout_btn = QPushButton('Выход')
        logout_btn.setFixedWidth(100)
        logout_btn.clicked.connect(self.logout)
        top_panel.addWidget(logout_btn)

        main_layout.addLayout(top_panel)

        # Панель управления (только для менеджера и администратора)
        if self.current_user['role_name'] in ['Менеджер', 'Администратор']:
            control_panel = QHBoxLayout()

            # Поиск
            search_label = QLabel('Поиск:')
            control_panel.addWidget(search_label)

            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText('Поиск по всем полям...')
            self.search_input.textChanged.connect(self.apply_filters)
            control_panel.addWidget(self.search_input, 2)

            # Фильтр по поставщику
            filter_label = QLabel('Поставщик:')
            control_panel.addWidget(filter_label)

            self.supplier_combo = QComboBox()
            self.supplier_combo.addItem('Все поставщики')
            self.load_suppliers()
            self.supplier_combo.currentTextChanged.connect(self.apply_filters)
            control_panel.addWidget(self.supplier_combo, 1)

            # Сортировка
            sort_label = QLabel('Сортировка:')
            control_panel.addWidget(sort_label)

            self.sort_combo = QComboBox()
            self.sort_combo.addItems(['Без сортировки', 'По количеству ↑', 'По количеству ↓'])
            self.sort_combo.currentTextChanged.connect(self.apply_filters)
            control_panel.addWidget(self.sort_combo, 1)

            main_layout.addLayout(control_panel)

        # Кнопки управления (только для администратора)
        if self.current_user['role_name'] == 'Администратор':
            buttons_layout = QHBoxLayout()

            add_product_btn = QPushButton('Добавить товар')
            add_product_btn.clicked.connect(self.add_product)
            buttons_layout.addWidget(add_product_btn)

            orders_btn = QPushButton('Заказы')
            orders_btn.clicked.connect(self.open_orders)
            buttons_layout.addWidget(orders_btn)

            buttons_layout.addStretch()
            main_layout.addLayout(buttons_layout)

        # Кнопка заказов для менеджера
        if self.current_user['role_name'] == 'Менеджер':
            orders_btn = QPushButton('Заказы')
            orders_btn.clicked.connect(self.open_orders)
            main_layout.addWidget(orders_btn)

        # Область прокрутки для карточек товаров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.products_container = QWidget()
        self.products_layout = QGridLayout(self.products_container)
        self.products_layout.setSpacing(15)

        scroll_area.setWidget(self.products_container)
        main_layout.addWidget(scroll_area)

        # Применяем стили
        try:
            with open('resources/styles.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except:
            pass

        # Центрирование окна
        self.center_window()

    def center_window(self):
        """Центрировать окно на экране"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def load_products(self):
        """Загрузка товаров из БД"""
        try:
            self.all_products = ProductQueries.get_all_products()
            self.filtered_products = self.all_products.copy()
            self.display_products()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки товаров:\n{str(e)}')

    def load_suppliers(self):
        """Загрузка списка поставщиков"""
        try:
            suppliers = ProductQueries.get_all_suppliers()
            for supplier in suppliers:
                self.supplier_combo.addItem(supplier['supplier_name'])
        except Exception as e:
            print(f'Ошибка загрузки поставщиков: {e}')

    def apply_filters(self):
        """Применение фильтров, поиска и сортировки"""
        # Начинаем с всех товаров
        result = self.all_products.copy()

        # Поиск (если доступен)
        if hasattr(self, 'search_input'):
            search_text = self.search_input.text().strip()
            if search_text:
                result = [p for p in result if
                         search_text.lower() in p['product_name'].lower() or
                         search_text.lower() in p['article'].lower() or
                         search_text.lower() in str(p.get('description', '')).lower() or
                         search_text.lower() in str(p.get('supplier_name', '')).lower() or
                         search_text.lower() in str(p.get('category_name', '')).lower()]

        # Фильтр по поставщику (если доступен)
        if hasattr(self, 'supplier_combo'):
            supplier = self.supplier_combo.currentText()
            if supplier != 'Все поставщики':
                result = [p for p in result if p['supplier_name'] == supplier]

        # Сортировка (если доступна)
        if hasattr(self, 'sort_combo'):
            sort_option = self.sort_combo.currentText()
            if sort_option == 'По количеству ↑':
                result.sort(key=lambda x: x['quantity_in_stock'])
            elif sort_option == 'По количеству ↓':
                result.sort(key=lambda x: x['quantity_in_stock'], reverse=True)

        self.filtered_products = result
        self.display_products()

    def display_products(self):
        """Отображение товаров в виде карточек"""
        # Очистка текущего содержимого
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Отображение товаров
        if not self.filtered_products:
            no_products_label = QLabel('Товары не найдены')
            no_products_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_products_label.setStyleSheet('font-size: 16px; color: #999;')
            self.products_layout.addWidget(no_products_label, 0, 0)
            return

        # Размещение карточек в сетке (4 колонки)
        columns = 4
        for index, product in enumerate(self.filtered_products):
            row = index // columns
            col = index % columns
            card = ProductCard(product, self.current_user['role_name'], self)
            self.products_layout.addWidget(card, row, col)

    def add_product(self):
        """Открыть диалог добавления товара"""
        if self.edit_dialog is not None:
            QMessageBox.warning(self, 'Предупреждение',
                              'Закройте текущее окно редактирования перед открытием нового!')
            return

        self.edit_dialog = ProductEditDialog(None, self)
        self.edit_dialog.finished.connect(self.on_edit_dialog_closed)
        self.edit_dialog.exec()

    def edit_product(self, product_id):
        """Открыть диалог редактирования товара"""
        if self.edit_dialog is not None:
            QMessageBox.warning(self, 'Предупреждение',
                              'Закройте текущее окно редактирования перед открытием нового!')
            return

        self.edit_dialog = ProductEditDialog(product_id, self)
        self.edit_dialog.finished.connect(self.on_edit_dialog_closed)
        self.edit_dialog.exec()

    def on_edit_dialog_closed(self):
        """Обработка закрытия диалога редактирования"""
        self.edit_dialog = None
        self.load_products()

    def open_orders(self):
        """Открыть окно заказов"""
        self.orders_window = OrdersWindow(self.current_user, self)
        self.orders_window.show()

    def logout(self):
        """Выход из системы"""
        self.login_window.show_login()
        self.close()
