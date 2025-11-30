from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from database.queries import OrderQueries
from views.order_edit_dialog import OrderEditDialog


class OrdersWindow(QMainWindow):
    """Окно управления заказами"""

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.current_user = user
        self.parent_window = parent
        self.edit_dialog = None
        self.init_ui()
        self.load_orders()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(f'Заказы - {self.current_user["full_name"]}')
        self.setMinimumSize(1200, 700)
        self.setWindowIcon(QIcon('resources/images/icon.ico'))

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Верхняя панель
        top_panel = QHBoxLayout()

        title = QLabel('Список заказов')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        top_panel.addWidget(title)

        top_panel.addStretch()

        # ФИО пользователя
        user_label = QLabel(f" {self.current_user['full_name']} ({self.current_user['role_name']})")
        user_label.setStyleSheet('font-weight: bold;')
        top_panel.addWidget(user_label)

        # Кнопка назад
        back_btn = QPushButton('Назад к товарам')
        back_btn.clicked.connect(self.close)
        top_panel.addWidget(back_btn)

        main_layout.addLayout(top_panel)

        # Кнопка добавления (только для администратора)
        if self.current_user['role_name'] == 'Администратор':
            add_order_btn = QPushButton('Добавить заказ')
            add_order_btn.setMinimumHeight(40)
            add_order_btn.clicked.connect(self.add_order)
            main_layout.addWidget(add_order_btn)

        # Таблица заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            'ID', 'Дата заказа', 'Дата доставки',
            'Пункт выдачи', 'Клиент', 'Статус', 'Код получения'
        ])

        # Настройка таблицы
        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.orders_table.setAlternatingRowColors(True)

        # Двойной клик для редактирования (только администратор)
        if self.current_user['role_name'] == 'Администратор':
            self.orders_table.doubleClicked.connect(self.edit_selected_order)

        main_layout.addWidget(self.orders_table)

        # Кнопки управления (только для администратора)
        if self.current_user['role_name'] == 'Администратор':
            buttons_layout = QHBoxLayout()

            edit_btn = QPushButton('Редактировать')
            edit_btn.setMinimumHeight(40)
            edit_btn.clicked.connect(self.edit_selected_order)
            buttons_layout.addWidget(edit_btn)

            delete_btn = QPushButton('Удалить')
            delete_btn.setObjectName('deleteButton')
            delete_btn.setMinimumHeight(40)
            delete_btn.clicked.connect(self.delete_selected_order)
            buttons_layout.addWidget(delete_btn)

            buttons_layout.addStretch()
            main_layout.addLayout(buttons_layout)

        # Информация для пользователя
        info_label = QLabel('Подсказка: Дважды щелкните по заказу для просмотра деталей' if self.current_user['role_name'] == 'Менеджер'
                           else 'Подсказка: Дважды щелкните по заказу для редактирования')
        info_label.setStyleSheet('color: #666; font-style: italic; padding: 10px;')
        main_layout.addWidget(info_label)

        try:
            with open('resources/styles.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except:
            pass

        self.center_window()

    def center_window(self):
        """Центрировать окно на экране"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def load_orders(self):
        """Загрузка заказов из БД"""
        try:
            orders = OrderQueries.get_all_orders()
            self.orders_table.setRowCount(len(orders))

            for row, order in enumerate(orders):
                self.orders_table.setItem(row, 0, QTableWidgetItem(str(order['order_id'])))
                self.orders_table.setItem(row, 1, QTableWidgetItem(str(order['order_date']).split()[0] if order.get('order_date') else ''))
                self.orders_table.setItem(row, 2, QTableWidgetItem(str(order['delivery_date']).split()[0] if order.get('delivery_date') else ''))
                self.orders_table.setItem(row, 3, QTableWidgetItem(order['pickup_address']))
                self.orders_table.setItem(row, 4, QTableWidgetItem(order['client_name']))
                status_item = QTableWidgetItem(order['status_name'])
                if order['status_name'] == 'Новый':
                    status_item.setBackground(Qt.GlobalColor.lightGray)
                elif order['status_name'] == 'Завершен':
                    status_item.setBackground(Qt.GlobalColor.green)
                self.orders_table.setItem(row, 5, status_item)
                self.orders_table.setItem(row, 6, QTableWidgetItem(order.get('recipient_code', '')))

                for col in range(7):
                    item = self.orders_table.item(row, col)
                    if item:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки заказов:\n{str(e)}')

    def add_order(self):
        """Открыть диалог добавления заказа"""
        if self.edit_dialog is not None:
            QMessageBox.warning(self, 'Предупреждение',
                              'Закройте текущее окно редактирования перед открытием нового!')
            return

        self.edit_dialog = OrderEditDialog(None, self)
        self.edit_dialog.finished.connect(self.on_edit_dialog_closed)
        self.edit_dialog.exec()

    def edit_selected_order(self):
        """Редактировать выбранный заказ"""
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите заказ для редактирования!')
            return

        if self.edit_dialog is not None:
            QMessageBox.warning(self, 'Предупреждение',
                              'Закройте текущее окно редактирования перед открытием нового!')
            return

        row = self.orders_table.currentRow()
        order_id = int(self.orders_table.item(row, 0).text())

        self.edit_dialog = OrderEditDialog(order_id, self)
        self.edit_dialog.finished.connect(self.on_edit_dialog_closed)
        self.edit_dialog.exec()

    def delete_selected_order(self):
        """Удалить выбранный заказ"""
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите заказ для удаления!')
            return

        row = self.orders_table.currentRow()
        order_id = int(self.orders_table.item(row, 0).text())
        client_name = self.orders_table.item(row, 4).text()

        reply = QMessageBox.question(
            self,
            'Подтверждение удаления',
            f'Вы действительно хотите удалить заказ #{order_id} ({client_name})?\nЭто действие необратимо!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                OrderQueries.delete_order(order_id)
                QMessageBox.information(self, 'Успех', 'Заказ успешно удален!')
                self.load_orders()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления заказа:\n{str(e)}')

    def on_edit_dialog_closed(self):
        """Обработка закрытия диалога редактирования"""
        self.edit_dialog = None
        self.load_orders()
