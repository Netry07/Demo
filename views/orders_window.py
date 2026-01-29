"""orders_window"""
import os

from PyQt6.QtWidgets import (
    QDialog,  # Изменено с QMainWindow на QDialog
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
from database.queries import OrderQueries


# --- Класс карточки заказа ---
class OrderCard(QFrame):
    def __init__(self, order, parent=None):
        super().__init__(parent)
        self.order = order
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)

        self.setStyleSheet(
            f".OrderCard {{ border: 1px solid black; background-color: {"white"}; margin-bottom: 5px; }}"
        )
        self.init_ui()

    def init_ui(self):
        # Основной горизонтальный layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Левая часть - основная информация
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        # Артикул заказа
        article = self.order.get('article', 'N/A')
        lbl_article = QLabel(f"Артикул заказа: {article}")
        lbl_article.setStyleSheet("background-color: transparent; font-family: Times New Roman; font-size: 12px;")
        left_layout.addWidget(lbl_article)

        # Статус заказа
        status = self.order.get('status_name', 'Не указан')
        lbl_status = QLabel(f"Статус заказа: {status}")
        lbl_status.setStyleSheet("background-color: transparent; font-family: Times New Roman; font-size: 12px;")
        left_layout.addWidget(lbl_status)

        # Адрес пункта выдачи
        pickup_address = self.order.get('pickup_address', 'Не указан')
        lbl_pickup = QLabel(f"Адрес пункта выдачи: {pickup_address}")
        lbl_pickup.setStyleSheet("background-color: transparent; font-family: Times New Roman; font-size: 12px;")
        left_layout.addWidget(lbl_pickup)

        # Дата заказа (формат год-месяц-день)
        order_date = self.order.get('order_date', 'Не указана')
        if order_date and order_date != 'Не указана':
            try:
                # Преобразуем дату в формат YYYY-MM-DD
                if isinstance(order_date, str):
                    from datetime import datetime
                    # Попытка распарсить различные форматы даты
                    for fmt in ['%Y-%m-%d', '%d.%m.%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            date_obj = datetime.strptime(str(order_date).split()[0], fmt)
                            order_date = date_obj.strftime('%Y-%m-%d')
                            break
                        except:
                            continue
                else:
                    order_date = order_date.strftime('%Y-%m-%d')
            except:
                pass  # Оставляем как есть, если не удалось преобразовать

        lbl_order_date = QLabel(f"Дата заказа: {order_date}")
        lbl_order_date.setStyleSheet("background-color: transparent; font-family: Times New Roman; font-size: 12px;")
        left_layout.addWidget(lbl_order_date)

        left_layout.addStretch()
        main_layout.addLayout(left_layout, stretch=3)

        # Правая часть - дата доставки
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Дата доставки (формат год-месяц-день)
        delivery_date = self.order.get('delivery_date', 'Не указана')
        if delivery_date and delivery_date != 'Не указана':
            try:
                # Преобразуем дату в формат YYYY-MM-DD
                if isinstance(delivery_date, str):
                    from datetime import datetime
                    # Попытка распарсить различные форматы даты
                    for fmt in ['%Y-%m-%d', '%d.%m.%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            date_obj = datetime.strptime(str(delivery_date).split()[0], fmt)
                            delivery_date = date_obj.strftime('%Y-%m-%d')
                            break
                        except:
                            continue
                else:
                    delivery_date = delivery_date.strftime('%Y-%m-%d')
            except:
                pass  # Оставляем как есть, если не удалось преобразовать

        lbl_delivery = QLabel(f"Дата доставки\n\n{delivery_date}")
        lbl_delivery.setStyleSheet("background-color: transparent; font-family: Times New Roman; font-size: 12px;")
        lbl_delivery.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_delivery.setWordWrap(True)
        right_layout.addWidget(lbl_delivery)

        right_layout.addStretch()
        main_layout.addLayout(right_layout, stretch=1)

    def mousePressEvent(self, event):
        """Обработка клика на карточку заказа"""
        if event.button() == Qt.MouseButton.LeftButton:
            parent_window = self.window()
            if hasattr(parent_window, 'on_order_card_clicked'):
                parent_window.on_order_card_clicked(self.order)
        super().mousePressEvent(event)


# --- Главное окно заказов ---
class OrdersWindow(QDialog):
    """Окно управления заказами"""

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.current_user = user
        self.all_orders = []
        self.filtered_orders = []

        self.setModal(True)  # Делаем окно модальным
        self.setStyleSheet("QDialog { background-color: white; }")
        self.init_ui()
        self.load_orders()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f'Заказы - {self.current_user["full_name"]}')
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(QIcon("resources/images/icon.ico"))

        # Основной layout
        main_layout = QVBoxLayout(self)

        # Верхняя панель
        top_panel_container = QWidget()
        top_panel_container.setStyleSheet("background-color: #7FFF00; border-radius: 5px;")

        top_panel_sublayout = QHBoxLayout(top_panel_container)

        logo_label = QLabel("Управление заказами")
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
        back_btn.clicked.connect(self.close_window)
        top_panel_sublayout.addWidget(back_btn)

        top_panel = QHBoxLayout()
        top_panel.addWidget(top_panel_container)

        main_layout.addLayout(top_panel)

        # Кнопки управления
        if self.current_user["role_name"] == "Администратор":
            buttons_layout = QHBoxLayout()

            add_order_btn = QPushButton("Добавить заказ")
            add_order_btn.setStyleSheet(
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
            add_order_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            add_order_btn.clicked.connect(self.add_order)
            buttons_layout.addWidget(add_order_btn)

            buttons_layout.addStretch()
            main_layout.addLayout(buttons_layout)

        # Область прокрутки для списка заказов
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
                    "QScrollArea { border: none; background-color: transparent; }"
        )
        self.orders_container = QWidget()
        self.orders_container.setStyleSheet("background-color: #7FFF00; border-radius: 5px;")
        self.orders_layout = QVBoxLayout(self.orders_container)
        self.orders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.orders_layout.setSpacing(10)

        self.scroll_area.setWidget(self.orders_container)
        main_layout.addWidget(self.scroll_area)

    def load_orders(self):
        """Загрузка заказов из БД"""
        try:
            self.all_orders = OrderQueries.get_all_orders()
            self.filtered_orders = self.all_orders.copy()
            self.display_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки заказов:\n{str(e)}")

    # def apply_filters(self):
    #     """Применение фильтров"""
    #     result = self.all_orders.copy()

    #     if hasattr(self, "search_input"):
    #         search_text = self.search_input.text().strip().lower()
    #         if search_text:
    #             result = [
    #                 o for o in result
    #                 if search_text in str(o.get("client_name", "")).lower()
    #                 or search_text in str(o.get("recipient_code", "")).lower()
    #                 or search_text in str(o.get("order_id", "")).lower()
    #             ]

    #     if hasattr(self, "status_combo"):
    #         status = self.status_combo.currentText()
    #         if status != "Все статусы":
    #             result = [o for o in result if o.get("status_name") == status]

    #     self.filtered_orders = result
    #     self.display_orders()

    def display_orders(self):
        """Отображение списка заказов"""
        # Очистка текущего списка
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.filtered_orders:
            no_data_label = QLabel("Заказы не найдены")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("font-family: Times New Roman; font-size: 16px;")
            self.orders_layout.addWidget(no_data_label)
            return

        for order in self.filtered_orders:
            card = OrderCard(order)
            if self.current_user["role_name"] == "Администратор":
                card.setCursor(Qt.CursorShape.PointingHandCursor)
            self.orders_layout.addWidget(card)

    def on_order_card_clicked(self, order):
        """Обработчик клика на карточку заказа"""
        if self.current_user["role_name"] == "Администратор":
            self.edit_order(order)

    def edit_order(self, order):
        """Открытие окна редактирования заказа"""
        from views.order_edit_dialog import OrderEditDialog

        dialog = OrderEditDialog(order["order_id"], self)
        if dialog.exec():
            self.load_orders()

    def add_order(self):
        """Добавление нового заказа"""
        from views.order_edit_dialog import OrderEditDialog

        dialog = OrderEditDialog(None, self)
        if dialog.exec():
            self.load_orders()

    def close_window(self):
        """Закрытие окна заказов"""
        self.accept()  # Используем accept() вместо close() для QDialog
