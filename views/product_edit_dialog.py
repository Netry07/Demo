import os
import shutil
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QSpinBox,
                             QDoubleSpinBox, QTextEdit, QFileDialog, QMessageBox,
                             QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from database.queries import ProductQueries
from PIL import Image


class ProductEditDialog(QDialog):
    """Диалог добавления/редактирования товара"""

    def __init__(self, product_id=None, parent=None):
        super().__init__(parent)
        self.product_id = product_id
        self.product_data = None
        self.new_photo_path = None
        self.old_photo_path = None

        if product_id:
            self.product_data = ProductQueries.get_product_by_id(product_id)
            self.old_photo_path = self.product_data.get('photo_path')

        self.init_ui()

        if self.product_data:
            self.load_product_data()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle('Редактирование товара' if self.product_id else 'Добавление товара')
        self.setMinimumSize(600, 700)
        self.setModal(True)

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel('Редактирование товара' if self.product_id else 'Добавление нового товара')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Форма
        form_layout = QFormLayout()

        # ID (только для просмотра при редактировании)
        if self.product_id:
            self.id_label = QLabel(str(self.product_id))
            form_layout.addRow('ID:', self.id_label)

        # Артикул
        self.article_input = QLineEdit()
        self.article_input.setPlaceholderText('Введите артикул')
        form_layout.addRow('Артикул*:', self.article_input)

        # Название
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите название товара')
        form_layout.addRow('Название*:', self.name_input)

        # Категория
        self.category_combo = QComboBox()
        self.load_categories()
        form_layout.addRow('Категория*:', self.category_combo)

        # Поставщик
        self.supplier_combo = QComboBox()
        self.load_suppliers()
        form_layout.addRow('Поставщик*:', self.supplier_combo)

        # Единица измерения
        self.unit_combo = QComboBox()
        self.load_units()
        form_layout.addRow('Ед. измерения*:', self.unit_combo)

        # Цена
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(' ₽')
        form_layout.addRow('Цена*:', self.price_input)

        # Скидка
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setDecimals(2)
        self.discount_input.setSuffix(' %')
        form_layout.addRow('Скидка:', self.discount_input)

        # Количество на складе
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 100000)
        form_layout.addRow('Количество*:', self.quantity_input)

        layout.addLayout(form_layout)

        # Описание
        desc_group = QGroupBox('Описание')
        desc_layout = QVBoxLayout()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Введите описание товара...')
        self.description_input.setMaximumHeight(100)
        desc_layout.addWidget(self.description_input)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)

        # Фото
        photo_group = QGroupBox('Фото товара')
        photo_layout = QVBoxLayout()

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(300, 200)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet('border: 1px solid #CCC; background-color: #F5F5F5;')
        self.load_photo_preview()
        photo_layout.addWidget(self.photo_label)

        photo_buttons = QHBoxLayout()
        change_photo_btn = QPushButton('Выбрать фото')
        change_photo_btn.clicked.connect(self.select_photo)
        photo_buttons.addWidget(change_photo_btn)

        remove_photo_btn = QPushButton('Удалить фото')
        remove_photo_btn.clicked.connect(self.remove_photo)
        photo_buttons.addWidget(remove_photo_btn)

        photo_layout.addLayout(photo_buttons)
        photo_group.setLayout(photo_layout)
        layout.addWidget(photo_group)

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton('Сохранить')
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_product)
        buttons_layout.addWidget(save_btn)

        if self.product_id:
            delete_btn = QPushButton('Удалить')
            delete_btn.setObjectName('deleteButton')
            delete_btn.setMinimumHeight(40)
            delete_btn.clicked.connect(self.delete_product)
            buttons_layout.addWidget(delete_btn)

        cancel_btn = QPushButton('Отмена')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_categories(self):
        """Загрузка категорий"""
        try:
            categories = ProductQueries.get_all_categories()
            for cat in categories:
                self.category_combo.addItem(cat['category_name'])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки категорий: {e}')

    def load_suppliers(self):
        """Загрузка поставщиков"""
        try:
            suppliers = ProductQueries.get_all_suppliers()
            for sup in suppliers:
                self.supplier_combo.addItem(sup['supplier_name'])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки поставщиков: {e}')

    def load_units(self):
        """Загрузка единиц измерения"""
        try:
            units = ProductQueries.get_all_units()
            for unit in units:
                self.unit_combo.addItem(unit['unit_name'])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки единиц: {e}')

    def load_product_data(self):
        """Загрузка данных товара в поля"""
        if not self.product_data:
            return

        self.article_input.setText(self.product_data['article'])
        self.name_input.setText(self.product_data['product_name'])
        self.price_input.setValue(float(self.product_data['price']))
        self.discount_input.setValue(float(self.product_data['current_discount']))
        self.quantity_input.setValue(self.product_data['quantity_in_stock'])
        self.description_input.setPlainText(self.product_data.get('description', ''))

        # Установка комбобоксов
        self.category_combo.setCurrentText(self.product_data['category_name'])
        self.supplier_combo.setCurrentText(self.product_data['supplier_name'])
        self.unit_combo.setCurrentText(self.product_data['unit_name'])

    def load_photo_preview(self):
        """Загрузка превью фото"""
        photo_path = None

        if self.new_photo_path:
            photo_path = self.new_photo_path
        elif self.product_data and self.product_data.get('photo_path'):
            photo_path = self.product_data['photo_path']

        if photo_path and os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
        else:
            pixmap = QPixmap('resources/images/picture.png')

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
            self.photo_label.setPixmap(scaled_pixmap)

    def select_photo(self):
        """Выбор фото товара"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            'Выберите фото товара',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp)'
        )

        if file_path:
            try:
                # Изменяем размер изображения до 300x200
                img = Image.open(file_path)
                img.thumbnail((300, 200), Image.Resampling.LANCZOS)

                # Создаем папку для товаров если её нет
                os.makedirs('resources/products', exist_ok=True)

                # Сохраняем с уникальным именем
                file_name = os.path.basename(file_path)
                new_path = f'resources/products/{file_name}'

                # Если файл уже существует, добавляем счетчик
                counter = 1
                while os.path.exists(new_path):
                    name, ext = os.path.splitext(file_name)
                    new_path = f'resources/products/{name}_{counter}{ext}'
                    counter += 1

                img.save(new_path)
                self.new_photo_path = new_path
                self.load_photo_preview()

            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка обработки изображения: {e}')

    def remove_photo(self):
        """Удаление фото"""
        self.new_photo_path = None
        self.load_photo_preview()

    def validate_inputs(self):
        """Валидация введенных данных"""
        if not self.article_input.text().strip():
            QMessageBox.warning(self, 'Ошибка', 'Введите артикул товара!')
            return False

        if not self.name_input.text().strip():
            QMessageBox.warning(self, 'Ошибка', 'Введите название товара!')
            return False

        if self.price_input.value() <= 0:
            QMessageBox.warning(self, 'Ошибка', 'Цена должна быть больше нуля!')
            return False

        return True

    def save_product(self):
        """Сохранение товара"""
        if not self.validate_inputs():
            return

        try:
            article = self.article_input.text().strip()
            name = self.name_input.text().strip()
            category = self.category_combo.currentText()
            supplier = self.supplier_combo.currentText()
            unit = self.unit_combo.currentText()
            price = self.price_input.value()
            discount = self.discount_input.value()
            quantity = self.quantity_input.value()
            description = self.description_input.toPlainText().strip()

            # Определяем путь к фото
            photo_path = self.new_photo_path
            if not photo_path and self.product_data:
                photo_path = self.product_data.get('photo_path')

            if self.product_id:
                # Обновление товара
                ProductQueries.update_product(
                    self.product_id, article, name, unit, price,
                    supplier, category, discount, quantity, description, photo_path
                )

                # Удаляем старое фото если было заменено
                if self.new_photo_path and self.old_photo_path and os.path.exists(self.old_photo_path):
                    try:
                        os.remove(self.old_photo_path)
                    except:
                        pass

                QMessageBox.information(self, 'Успех', 'Товар успешно обновлен!')
            else:
                # Добавление нового товара
                ProductQueries.add_product(
                    article, name, unit, price,
                    supplier, category, discount, quantity, description, photo_path
                )
                QMessageBox.information(self, 'Успех', 'Товар успешно добавлен!')

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения товара:\n{str(e)}')

    def delete_product(self):
        """Удаление товара"""
        reply = QMessageBox.question(
            self,
            'Подтверждение удаления',
            'Вы действительно хотите удалить этот товар?\nЭто действие необратимо!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                ProductQueries.delete_product(self.product_id)

                # Удаляем фото если оно есть
                if self.old_photo_path and os.path.exists(self.old_photo_path):
                    try:
                        os.remove(self.old_photo_path)
                    except:
                        pass

                QMessageBox.information(self, 'Успех', 'Товар успешно удален!')
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления товара:\n{str(e)}')
