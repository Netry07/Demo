import os
"""products_window"""
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QScrollArea,
    QFrame,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from database.queries import ProductQueries
from views.orders_window import OrdersWindow

SCROLLBAR_STYLE = """
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #A9A9A9;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #808080;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #A9A9A9;
    border-radius: 5px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background: #808080;
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""

COMBOBOX_STYLE = """
QComboBox {
    background-color: white;
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    padding: 5px 10px;
    font-family: Times New Roman;
    font-size: 14px;
    min-height: 25px;
}
QComboBox:hover {
    border: 1px solid #00FA9A;
}
QComboBox:focus {
    border: 1px solid #00FA9A;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: url(resources/images/arrow_down.png);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    selection-background-color: #00FA9A;
    selection-color: black;
    font-family: Times New Roman;
    font-size: 14px;
    padding: 5px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    min-height: 30px;
    padding: 5px 10px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #E0FFE0;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #00FA9A;
    color: black;
}
"""

LINEEDIT_STYLE = """
QLineEdit {
    background-color: white;
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    padding: 5px 10px;
    font-family: Times New Roman;
    font-size: 14px;
    min-height: 25px;
}
QLineEdit:hover {
    border: 1px solid #00FA9A;
}
QLineEdit:focus {
    border: 2px solid #00FA9A;
    padding: 4px 9px;
}
"""

# --- Класс карточки товара ---
class ProductCard(QFrame):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        # Настройка внешнего вида рамки
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)

        self.setMinimumHeight(150)  # Минимальная высота
        self.setMaximumHeight(180)  # Максимальная высота

        # Базовый стиль
        bg_color = "white"
        # 2. Если скидка > 15%, фон меняется на #2E8B57
        # Важно: > 15 (строго больше, 15 не включается)
        if product.get("current_discount", 0) > 15:
            bg_color = "#2E8B57"

        # Фон карточки явно задан (белый или #2E8B57), поэтому он не наследует фон окна
        self.setStyleSheet(
            f".ProductCard {{ border: 1px solid black; background-color: {bg_color}; margin-bottom: 5px; }}"
        )

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # 1. Левая часть - Фото
        photo_container = QLabel()
        photo_container.setFixedSize(100, 100)
        photo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_container.setStyleSheet("border: 1px solid black; background-color: white; color: black;")

        photo_path = self.product.get("photo_path")
        if photo_path and os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
        else:
            pixmap = QPixmap("resources/images/picture.png")
        photo_container.setPixmap(
            pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio)
        )

        main_layout.addWidget(photo_container)

        # 2. Центральная часть - Информация
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # Заголовок
        header_text = f"{self.product.get('category_name', 'Нет категории')} | {self.product.get('product_name', 'Без названия')}"
        lbl_header = QLabel(header_text)
        lbl_header.setTextFormat(Qt.TextFormat.RichText)
        lbl_header.setStyleSheet("font-family: Times New Roman; font-size: 14px; background-color: transparent;")
        info_layout.addWidget(lbl_header)

        # Описание
        desc = self.product.get("description")
        lbl_desc = QLabel(f"Описание товара: {desc if desc else ''}")
        lbl_desc.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
        info_layout.addWidget(lbl_desc)

        # Производитель
        lbl_prod = QLabel(
            f"Производитель: {self.product.get('manufacturer', 'Не указан')}"
        )
        lbl_prod.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
        info_layout.addWidget(lbl_prod)

        # Поставщик
        lbl_supp = QLabel(
            f"Поставщик: {self.product.get('supplier_name', 'Не указан')}"
        )
        lbl_supp.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
        info_layout.addWidget(lbl_supp)

        # --- ЦЕНА (Пункт 1) ---
        price = self.product.get("price", 0)
        discount = self.product.get("current_discount", 0)
        price_with_discount = self.product.get("price_with_discount", 0)

        if discount > 0:
            # Старая цена красная и зачеркнутая, новая рядом черная
            price_text = (
                f"Цена: <span style='color: red; text-decoration: line-through;'>{price:.2f}</span> "
                f"{price_with_discount:.2f} ₽"
            )
        else:
            price_text = f"Цена: {price:.2f} ₽"

        lbl_price = QLabel(price_text)
        lbl_price.setTextFormat(Qt.TextFormat.RichText)  # Важно для HTML
        lbl_price.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
        info_layout.addWidget(lbl_price)

        # Единица измерения
        lbl_unit = QLabel(f"Единица измерения: {self.product.get('unit_name', 'шт.')}")
        lbl_unit.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
        info_layout.addWidget(lbl_unit)

        # --- КОЛИЧЕСТВО (Пункт 3) ---
        qty = self.product.get("quantity_in_stock", 0)
        lbl_qty = QLabel(f"Количество на складе: {qty}")
        lbl_qty.setStyleSheet("font-family: Times New Roman; background-color: transparent;")

        # Если 0, красим только строку (лейбл), а не всю карточку
        if qty == 0:
            lbl_qty.setStyleSheet(
                "font-family: Times New Roman; background-color: #87CEEB; border: 1px solid gray; padding: 2px;"
            )

        info_layout.addWidget(lbl_qty)
        info_layout.addStretch()
        main_layout.addLayout(info_layout, stretch=1)

        # 3. Правая часть - Скидка
        right_layout = QVBoxLayout()
        if discount > 0:
            discount_text = f"Действующая\nскидка\n{discount:.0f}%"
            lbl_discount = QLabel(discount_text)
            lbl_discount.setStyleSheet("font-family: Times New Roman; background-color: transparent;")
            lbl_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)
            right_layout.addWidget(lbl_discount)
        else:
            # Пустой виджет, чтобы структура не ломалась
            right_layout.addStretch()

        main_layout.addLayout(right_layout)

    def mousePressEvent(self, event):
        """Обработка клика на карточку товара"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Передаем событие родительскому окну
            parent_window = self.window()
            if hasattr(parent_window, "on_product_card_clicked"):
                parent_window.on_product_card_clicked(self.product)
        super().mousePressEvent(event)


# --- Главное окно ---
class ProductsWindow(QMainWindow):
    """Главное окно со списком товаров"""

    def __init__(self, user, login_window):
        super().__init__()
        self.current_user = user
        self.login_window = login_window
        self.all_products = []
        self.filtered_products = []
        self.init_ui()
        self.load_products()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f'Список товаров - {self.current_user["full_name"]}')
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(QIcon("resources/images/icon.ico"))

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 🟢 1. Устанавливаем фон для всего центрального виджета (окна)
        central_widget.setStyleSheet(
            f"QWidget {{ background-color: white; }}" # Ваш зеленый цвет
        )


        # Верхняя панель
        top_panel_container = QWidget()
        top_panel_container.setStyleSheet("background-color: #7FFF00; border-radius: 5px;")

        top_panel_sublayout = QHBoxLayout(top_panel_container)

        logo_label = QLabel("Магазин")
        logo_label.setStyleSheet(
            "font-family: Times New Roman; font-size: 24px; font-weight: bold;"
        )
        top_panel_sublayout.addWidget(logo_label)
        top_panel_sublayout.addStretch()

        user_label = QLabel(
            f"{self.current_user['full_name']} ({self.current_user['role_name']})"
        )
        user_label.setStyleSheet(
            "font-family: Times New Roman; font-weight: bold; font-size: 14px;"
        )
        top_panel_sublayout.addWidget(user_label)

        back_btn = QPushButton("Назад")
        back_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #00FA9A;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
                font-family: Times New Roman;
            }
            """
        )
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.logout)
        top_panel_sublayout.addWidget(back_btn)
        
        top_panel = QHBoxLayout()
        top_panel.addWidget(top_panel_container)

        main_layout.addLayout(top_panel)

        # Панель управления
        if self.current_user["role_name"] in ["Менеджер", "Администратор"]:
            control_panel_container = QWidget()
            control_panel_container.setStyleSheet("background-color: #7FFF00; border-radius: 5px;")

            control_panel_sublayout = QHBoxLayout(control_panel_container)

            control_panel_subcontainer = QWidget()
            control_panel_subcontainer.setStyleSheet("background-color: white; border-radius: 5px;")

            control_panel_subsublayout = QHBoxLayout(control_panel_subcontainer)

            search_label = QLabel("Поиск:")
            search_label.setStyleSheet("background-color: white; font-family: Times New Roman;")
            control_panel_subsublayout.addWidget(search_label)

            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Поиск по всем полям...")
            self.search_input.setStyleSheet(LINEEDIT_STYLE)
            self.search_input.textChanged.connect(self.apply_filters)
            control_panel_subsublayout.addWidget(self.search_input, 2)

            filter_label = QLabel("Поставщик:")
            filter_label.setStyleSheet("font-family: Times New Roman;")
            control_panel_subsublayout.addWidget(filter_label)

            self.supplier_combo = QComboBox()
            self.supplier_combo.addItem("Все поставщики")
            self.supplier_combo.setStyleSheet(COMBOBOX_STYLE)
            self.supplier_combo.setCursor(Qt.CursorShape.PointingHandCursor)
            self.load_suppliers()
            self.supplier_combo.currentTextChanged.connect(self.apply_filters)
            control_panel_subsublayout.addWidget(self.supplier_combo, 1)

            sort_label = QLabel("Сортировка:")
            sort_label.setStyleSheet("font-family: Times New Roman;")
            control_panel_subsublayout.addWidget(sort_label)

            self.sort_combo = QComboBox()
            self.sort_combo.setStyleSheet(COMBOBOX_STYLE)
            self.sort_combo.setCursor(Qt.CursorShape.PointingHandCursor)
            self.sort_combo.addItems(
                ["Без сортировки", "По количеству возр.", "По количеству убыв."]
            )
            self.sort_combo.currentTextChanged.connect(self.apply_filters)
            control_panel_subsublayout.addWidget(self.sort_combo, 1)

            control_panel_sublayout.addWidget(control_panel_subcontainer)

            control_panel = QHBoxLayout()
            control_panel.addWidget(control_panel_container)

            main_layout.addLayout(control_panel)

        # Кнопки управления
        if self.current_user["role_name"] in ["Менеджер", "Администратор"]:
            buttons_layout = QHBoxLayout()

            if self.current_user["role_name"] == "Администратор":
                add_product_btn = QPushButton("Добавить товар")
                add_product_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #00FA9A;
                        padding: 10px 20px;
                        border-radius: 5px;
                        font-family: Times New Roman;
                        font-size: 14px;
                    }
                    """
                )
                add_product_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                add_product_btn.clicked.connect(self.add_product)
                buttons_layout.addWidget(add_product_btn)

            orders_btn = QPushButton("Заказы")
            orders_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #00FA9A;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-family: Times New Roman;
                    font-size: 14px;
                }
                """
            )
            orders_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            orders_btn.clicked.connect(self.open_orders)
            buttons_layout.addWidget(orders_btn)

            buttons_layout.addStretch()
            main_layout.addLayout(buttons_layout)

        # --- СПИСОК КАРТОЧЕК ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(SCROLLBAR_STYLE)

        self.products_container = QWidget()
        self.products_container.setStyleSheet("background-color: #7FFF00; border-radius: 5px;")
        self.products_layout = QVBoxLayout(self.products_container)
        self.products_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.products_layout.setSpacing(10)

        self.scroll_area.setWidget(self.products_container)
        main_layout.addWidget(self.scroll_area)

        self.center_window()

    def center_window(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def load_products(self):
        try:
            self.all_products = ProductQueries.get_all_products()
            self.filtered_products = self.all_products.copy()
            self.display_products()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров:\n{str(e)}")

    def load_suppliers(self):
        try:
            suppliers = ProductQueries.get_all_suppliers()
            for supplier in suppliers:
                self.supplier_combo.addItem(supplier["supplier_name"])
        except Exception as e:
            print(f"Ошибка загрузки поставщиков: {e}")

    def apply_filters(self):
        """Применение фильтров и поиска"""
        result = self.all_products.copy()

        # Обработка поиска
        if hasattr(self, "search_input"):
            search_query = self.search_input.text().strip()
            if search_query:
                result = self._apply_smart_search(result, search_query)

        # Фильтр по поставщику
        if hasattr(self, "supplier_combo"):
            supplier = self.supplier_combo.currentText()
            if supplier != "Все поставщики":
                result = [p for p in result if p["supplier_name"] == supplier]

        # Сортировка
        if hasattr(self, "sort_combo"):
            sort_option = self.sort_combo.currentText()
            if "возр" in sort_option:
                result.sort(key=lambda x: x["quantity_in_stock"])
            elif "убыв" in sort_option:
                result.sort(key=lambda x: x["quantity_in_stock"], reverse=True)

        self.filtered_products = result
        self.display_products()


    def _is_gender_word(self, word: str) -> bool:
        """Проверяет, является ли слово указанием пола"""
        return word.startswith("муж") or word.startswith("жен")


    def _get_gender_prefix(self, word: str) -> str:
        """Получает префикс пола (первые 3 символа)"""
        if word.startswith("муж"):
            return "муж"
        elif word.startswith("жен"):
            return "жен"
        return None


    def _apply_smart_search(self, products: list, search_query: str) -> list:
        """
        Умный поиск по товарам с поддержкой:
        - Точного совпадения названия товара
        - Поиска по категории (включая гендерные префиксы)
        - Комбинированного поиска (название + категория)
        """
        search_lower = search_query.lower()
        search_words = search_lower.split()

        # Если запрос пустой
        if not search_words:
            return products

        # Одно слово в запросе
        if len(search_words) == 1:
            word = search_words[0]

            if self._is_gender_word(word):
                # Поиск по гендерному префиксу в категории
                prefix = self._get_gender_prefix(word)
                return [
                    p for p in products
                    if p["product_name"].lower() == word
                    or prefix in p.get("category_name", "").lower()
                ]
            else:
                # Обычный поиск по названию или категории
                return [
                    p for p in products
                    if p["product_name"].lower() == word
                    or word in p.get("category_name", "").lower()
                    or word in p.get("article", "").lower()
                    or word in str(p.get("description", "")).lower()
                    or word in p.get("supplier_name", "").lower()
                ]
    
        # Несколько слов в запросе
        else:
            matching_products = []

            # Вариант 1: Одно слово - точное название, остальные - категория
            for name_word in search_words:
                other_words = [w for w in search_words if w != name_word]

                if other_words:
                    # Проверяем товары, где name_word точно совпадает с названием
                    for product in products:
                        if product["product_name"].lower() == name_word:
                            # Проверяем, что все остальные слова есть в категории
                            category_lower = product.get("category_name", "").lower()
                            all_match = True

                            for cat_word in other_words:
                                if self._is_gender_word(cat_word):
                                    prefix = self._get_gender_prefix(cat_word)
                                    if prefix not in category_lower:
                                        all_match = False
                                        break
                                else:
                                    if cat_word not in category_lower:
                                        all_match = False
                                        break
                                    
                            if all_match and product not in matching_products:
                                matching_products.append(product)

            # Вариант 2: Все слова в категории
            for product in products:
                category_lower = product.get("category_name", "").lower()
                all_in_category = True

                for cat_word in search_words:
                    if self._is_gender_word(cat_word):
                        prefix = self._get_gender_prefix(cat_word)
                        if prefix not in category_lower:
                            all_in_category = False
                            break
                    else:
                        if cat_word not in category_lower:
                            all_in_category = False
                            break
                        
                if all_in_category and product not in matching_products:
                    matching_products.append(product)
        
        return matching_products

    def display_products(self):
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.filtered_products:
            no_data_label = QLabel("Товары не найдены")
            no_data_label.setStyleSheet("font-family: Times New Roman;")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_layout.addWidget(no_data_label)
            return

        for product in self.filtered_products:
            card = ProductCard(product)
            # Делаем карточку кликабельной
            if self.current_user["role_name"] == "Администратор":
                card.setCursor(Qt.CursorShape.PointingHandCursor)
            self.products_layout.addWidget(card)

    def on_product_card_clicked(self, product):
        """Обработчик клика на карточку товара"""
        # Только администратор может редактировать товары
        if self.current_user["role_name"] == "Администратор":
            self.edit_product(product)

    def edit_product(self, product):
        """Открытие окна редактирования товара"""
        from views.product_edit_dialog import ProductEditDialog

        dialog = ProductEditDialog(product["product_id"], self)
        if dialog.exec():
            self.load_products()

    def add_product(self):
        from views.product_edit_dialog import ProductEditDialog

        dialog = ProductEditDialog(None, self)
        if dialog.exec():
            self.load_products()

    def open_orders(self):
        self.orders_window = OrdersWindow(self.current_user, self)
        self.orders_window.show()

    def logout(self):
        self.login_window.show_login()
        self.close()
