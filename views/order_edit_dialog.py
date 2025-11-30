from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QDateEdit,
                             QMessageBox, QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt, QDate
from database.queries import OrderQueries, UserQueries


class OrderEditDialog(QDialog):
    """Диалог добавления/редактирования заказа"""

    def __init__(self, order_id=None, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.order_data = None

        if order_id:
            self.order_data = OrderQueries.get_order_by_id(order_id)

        self.init_ui()

        if self.order_data:
            self.load_order_data()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle('Редактирование заказа' if self.order_id else 'Добавление заказа')
        self.setMinimumSize(600, 500)
        self.setModal(True)

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel('Редактирование заказа' if self.order_id else 'Добавление нового заказа')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Форма
        form_layout = QFormLayout()

        if self.order_id:
            self.id_label = QLabel(str(self.order_id))
            form_layout.addRow('ID:', self.id_label)

        # Артикул заказа
        self.order_code_input = QLineEdit()
        self.order_code_input.setPlaceholderText('Автоматически генерируется')
        self.order_code_input.setEnabled(False)  # Не редактируется
        form_layout.addRow('Артикул заказа:', self.order_code_input)

        # Дата заказа
        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDate(QDate.currentDate())
        self.order_date_input.setDisplayFormat('dd.MM.yyyy')
        form_layout.addRow('Дата заказа*:', self.order_date_input)

        # Дата доставки
        self.delivery_date_input = QDateEdit()
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDate(QDate.currentDate().addDays(7))
        self.delivery_date_input.setDisplayFormat('dd.MM.yyyy')
        form_layout.addRow('Дата доставки*:', self.delivery_date_input)

        # Пункт выдачи
        self.pickup_point_combo = QComboBox()
        self.load_pickup_points()
        form_layout.addRow('Пункт выдачи*:', self.pickup_point_combo)

        # Клиент
        self.client_combo = QComboBox()
        self.load_clients()
        form_layout.addRow('Клиент*:', self.client_combo)

        # Код получения
        self.receive_code_input = QLineEdit()
        self.receive_code_input.setPlaceholderText('Например: 901')
        self.receive_code_input.setMaxLength(10)
        form_layout.addRow('Код получения*:', self.receive_code_input)

        # Статус заказа
        self.status_combo = QComboBox()
        self.load_statuses()
        form_layout.addRow('Статус*:', self.status_combo)

        layout.addLayout(form_layout)

        # Информация
        info_group = QGroupBox('Справка')
        info_layout = QVBoxLayout()
        info_text = QLabel(
            '• Артикул заказа - уникальный идентификатор заказа\n'
            '• Дата доставки должна быть позже даты заказа\n'
            '• Код получения - числовой код для выдачи заказа клиенту\n'
            '• Все поля, отмеченные *, обязательны для заполнения'
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet('color: #666; font-size: 12px;')
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        layout.addStretch()

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton('Сохранить')
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_order)
        buttons_layout.addWidget(save_btn)

        if self.order_id:
            delete_btn = QPushButton('Удалить')
            delete_btn.setObjectName('deleteButton')
            delete_btn.setMinimumHeight(40)
            delete_btn.clicked.connect(self.delete_order)
            buttons_layout.addWidget(delete_btn)

        cancel_btn = QPushButton('Отмена')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_pickup_points(self):
        """Загрузка пунктов выдачи"""
        try:
            points = OrderQueries.get_all_pickup_points()
            for point in points:
                self.pickup_point_combo.addItem(point['full_address'], point['point_id'])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки пунктов выдачи: {e}')

    def load_clients(self):
        """Загрузка клиентов"""
        try:
            users = UserQueries.get_all_users()
            for user in users:
                display_text = f"{user['full_name']} ({user['role_name']})"
                self.client_combo.addItem(display_text, user['user_id'])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки клиентов: {e}')

    def load_statuses(self):
        """Загрузка статусов заказов"""
        try:
            # Статусы захардкожены, так как нет отдельной таблицы
            self.status_combo.addItem('Новый')
            self.status_combo.addItem('Завершен')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки статусов: {e}')

    def load_order_data(self):
        """Загрузка данных заказа в поля"""
        if not self.order_data:
            return

        self.receive_code_input.setText(self.order_data['recipient_code'])
        self.order_date_input.setDate(QDate.fromString(str(self.order_data['order_date']).split()[0], 'yyyy-MM-dd'))

        if self.order_data.get('delivery_date'):
            self.delivery_date_input.setDate(QDate.fromString(str(self.order_data['delivery_date']).split()[0], 'yyyy-MM-dd'))

        # Установка комбобоксов по ID
        pickup_index = self.pickup_point_combo.findData(self.order_data['pickup_point_id'])
        if pickup_index >= 0:
            self.pickup_point_combo.setCurrentIndex(pickup_index)

        client_index = self.client_combo.findData(self.order_data['user_id'])
        if client_index >= 0:
            self.client_combo.setCurrentIndex(client_index)

        # Статус - по тексту
        status_index = self.status_combo.findText(self.order_data['status_name'])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)

    def validate_inputs(self):
        """Валидация введенных данных"""
        if not self.receive_code_input.text().strip():
            QMessageBox.warning(self, 'Ошибка', 'Введите код получения!')
            return False

        # Проверка дат
        order_date = self.order_date_input.date()
        delivery_date = self.delivery_date_input.date()

        if delivery_date < order_date:
            QMessageBox.warning(
                self,
                'Ошибка',
                'Дата доставки не может быть раньше даты заказа!\n'
                'Пожалуйста, исправьте даты.'
            )
            return False

        return True

    def save_order(self):
        """Сохранение заказа"""
        if not self.validate_inputs():
            return

        try:
            order_date = self.order_date_input.date().toString('yyyy-MM-dd')
            delivered_at = self.delivery_date_input.date().toString('yyyy-MM-dd')
            pickup_point_id = self.pickup_point_combo.currentData()
            user_id = self.client_combo.currentData()
            receive_code = self.receive_code_input.text().strip()
            status = self.status_combo.currentText()
            client_name = self.client_combo.currentText().split(' (')[0]

            if self.order_id:
                # Обновление заказа
                OrderQueries.update_order(
                    self.order_id, pickup_point_id, order_date, delivered_at,
                    client_name, receive_code, status
                )
                QMessageBox.information(self, 'Успех', 'Заказ успешно обновлен!')
            else:
                # Добавление нового заказа
                OrderQueries.add_order(
                    user_id, pickup_point_id, order_date, delivered_at,
                    client_name, receive_code, status
                )
                QMessageBox.information(self, 'Успех', 'Заказ успешно добавлен!')

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения заказа:\n{str(e)}')

    def delete_order(self):
        """Удаление заказа"""
        reply = QMessageBox.question(
            self,
            'Подтверждение удаления',
            'Вы действительно хотите удалить этот заказ?\nЭто действие необратимо!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                OrderQueries.delete_order(self.order_id)
                QMessageBox.information(self, 'Успех', 'Заказ успешно удален!')
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления заказа:\n{str(e)}')
