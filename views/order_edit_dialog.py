"""order_edit_dialog"""
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDateEdit,
    QMessageBox,
    QFormLayout,
    QGroupBox,
)
from PyQt6.QtCore import Qt, QDate
from database.queries import OrderQueries, UserQueries


class OrderEditDialog(QDialog):
    """Диалог добавления/редактирования заказа"""

    def __init__(self, order_id=None, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.order_data = None

        # Загружаем данные сразу, если это редактирование
        if order_id:
            try:
                self.order_data = OrderQueries.get_order_by_id(order_id)
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка БД", f"Не удалось получить данные заказа: {e}"
                )

        self.init_ui()

        if self.order_data:
            self.load_order_data()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle(
            "Редактирование заказа" if self.order_id else "Добавление заказа"
        )
        self.setMinimumSize(600, 500)
        self.setModal(True)
        self.setStyleSheet("font-family: Times New Roman")

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel(
            "Редактирование заказа" if self.order_id else "Добавление нового заказа"
        )
        title.setStyleSheet(
            "font-family: Times New Roman; font-size: 18px; font-weight: bold;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Форма
        form_layout = QFormLayout()

        if self.order_id:
            self.id_label = QLabel(str(self.order_id))
            form_layout.addRow("ID:", self.id_label)

        # Артикул заказа - только для отображения
        if self.order_id:
            # При редактировании показываем текущий артикул как нередактируемое поле
            self.order_article_label = QLabel()
            self.order_article_label.setStyleSheet(
                "background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; font-family: Times New Roman; padding: 5px;"
            )
            form_layout.addRow("Артикул заказа:", self.order_article_label)
        else:
            # При создании показываем информацию об автогенерации
            article_info = QLabel("Будет сгенерирован автоматически")
            article_info.setStyleSheet(
                "background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; font-family: Times New Roman; padding: 5px;"
            )
            form_layout.addRow("Артикул заказа:", article_info)

        # Дата заказа
        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDate(QDate.currentDate())
        self.order_date_input.setDisplayFormat("dd.MM.yyyy")
        self.order_date_input.setStyleSheet("font-family: Times New Roman;")
        form_layout.addRow("Дата заказа*:", self.order_date_input)

        # Дата доставки
        self.delivery_date_input = QDateEdit()
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDate(QDate.currentDate().addDays(7))
        self.delivery_date_input.setDisplayFormat("dd.MM.yyyy")
        self.delivery_date_input.setStyleSheet("font-family: Times New Roman;")
        form_layout.addRow("Дата доставки*:", self.delivery_date_input)

        # Пункт выдачи
        self.pickup_point_combo = QComboBox()
        self.pickup_point_combo.setStyleSheet("font-family: Times New Roman;")
        self.load_pickup_points()
        form_layout.addRow("Пункт выдачи*:", self.pickup_point_combo)

        # Клиент
        self.client_combo = QComboBox()
        self.client_combo.setStyleSheet("font-family: Times New Roman;")
        self.load_clients()
        form_layout.addRow("Клиент*:", self.client_combo)

        # Код получения
        self.receive_code_input = QLineEdit()
        self.receive_code_input.setPlaceholderText("Например: 901")
        self.receive_code_input.setMaxLength(10)
        self.receive_code_input.setStyleSheet("font-family: Times New Roman;")
        form_layout.addRow("Код получения*:", self.receive_code_input)

        # Статус заказа
        self.status_combo = QComboBox()
        self.status_combo.setStyleSheet("font-family: Times New Roman;")
        self.load_statuses()
        form_layout.addRow("Статус*:", self.status_combo)

        layout.addLayout(form_layout)

        layout.addStretch()

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton("Сохранить")
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet(
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
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_order)
        buttons_layout.addWidget(save_btn)

        if self.order_id:
            delete_btn = QPushButton("Удалить")
            delete_btn.setMinimumHeight(40)
            delete_btn.setStyleSheet(
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
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.clicked.connect(self.delete_order)
            buttons_layout.addWidget(delete_btn)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet(
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
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_pickup_points(self):
        try:
            points = OrderQueries.get_all_pickup_points()
            for point in points:
                # Сохраняем ID как UserData
                self.pickup_point_combo.addItem(
                    point["full_address"], point["point_id"]
                )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки пунктов: {e}")

    def load_clients(self):
        try:
            users = UserQueries.get_all_users()
            for user in users:
                display_text = f"{user['full_name']} ({user['role_name']})"
                # Сохраняем ID как UserData
                self.client_combo.addItem(display_text, user["user_id"])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки клиентов: {e}")

    def load_statuses(self):
        # Статусы лучше вынести в отдельный справочник или Enum
        statuses = ["Новый", "В обработке", "Готов к выдаче", "Завершен", "Отменен"]
        self.status_combo.addItems(statuses)

    def load_order_data(self):
        """Заполнение полей данными из БД"""
        if not self.order_data:
            return

        # Отображаем артикул (только для чтения)
        if hasattr(self, 'order_article_label'):
            self.order_article_label.setText(self.order_data["article"])

        # Безопасное получение данных
        self.receive_code_input.setText(str(self.order_data.get("recipient_code", "")))

        # Обработка дат (преобразование в строку, отсечение времени, парсинг)
        try:
            o_date = str(self.order_data["order_date"]).split()[0]
            self.order_date_input.setDate(QDate.fromString(o_date, "yyyy-MM-dd"))

            if self.order_data.get("delivery_date"):
                d_date = str(self.order_data["delivery_date"]).split()[0]
                self.delivery_date_input.setDate(QDate.fromString(d_date, "yyyy-MM-dd"))
        except Exception:
            pass  # Оставляем текущую дату, если ошибка парсинга

        # Установка комбобоксов
        pickup_idx = self.pickup_point_combo.findData(
            self.order_data.get("pickup_point_id")
        )
        if pickup_idx >= 0:
            self.pickup_point_combo.setCurrentIndex(pickup_idx)

        client_idx = self.client_combo.findData(self.order_data.get("user_id"))
        if client_idx >= 0:
            self.client_combo.setCurrentIndex(client_idx)

        status_idx = self.status_combo.findText(self.order_data.get("status_name"))
        if status_idx >= 0:
            self.status_combo.setCurrentIndex(status_idx)

    def save_order(self):
        """Сохранение заказа"""
        order_date = self.order_date_input.date().toPyDate()
        delivery_date = self.delivery_date_input.date().toPyDate()
        data = {
            "pickup_point_id": self.pickup_point_combo.currentData(),
            "user_id": self.client_combo.currentData(),
            "order_date": order_date,
            "delivery_date": delivery_date,
            "recipient_code": self.receive_code_input.text().strip(),
            "status_name": self.status_combo.currentText(),
            "client_name": self.client_combo.currentText().split(" (")[0],
        }
        if self.order_id:
            OrderQueries.update_order(
                self.order_id,
                self.order_data["article"],
                data["pickup_point_id"],
                data["order_date"],
                data["delivery_date"],
                data["client_name"],
                data["recipient_code"],
                data["status_name"],
            )
            QMessageBox.information(self, "Успех", "Заказ успешно обновлен!")
        else:
            OrderQueries.add_order(
                "",  # Пустая строка = автогенерация артикула
                data["user_id"],
                data["pickup_point_id"],
                data["order_date"],
                data["delivery_date"],
                data["client_name"],
                data["recipient_code"],
                data["status_name"],
            )
            QMessageBox.information(self, "Успех", "Заказ успешно добавлен!")
        self.accept()

    def delete_order(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить заказ? Это необратимо!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                OrderQueries.delete_order(self.order_id)
                QMessageBox.information(self, "Успех", "Заказ успешно удален!")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить:\n{e}")
