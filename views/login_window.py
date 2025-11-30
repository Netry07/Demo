from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from database.queries import UserQueries
from views.products_window import ProductsWindow


class LoginWindow(QWidget):
    """Окно авторизации пользователя"""

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle('Авторизация - Магазин обуви')
        self.setFixedSize(400, 500)
        self.setWindowIcon(QIcon('resources/images/icon.ico'))

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Логотип
        logo_label = QLabel()
        try:
            pixmap = QPixmap('resources/images/logo.png')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except:
            logo_label.setText('🏪 Магазин обуви')
            logo_label.setStyleSheet('font-size: 24px; font-weight: bold;')

        main_layout.addWidget(logo_label)
        main_layout.addSpacing(30)

        # Заголовок
        title_label = QLabel('Вход в систему')
        title_label.setStyleSheet('font-size: 18px; font-weight: bold;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)

        # Поле логина
        login_label = QLabel('Логин:')
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText('Введите логин')
        self.login_input.setMinimumHeight(35)

        main_layout.addWidget(login_label)
        main_layout.addWidget(self.login_input)
        main_layout.addSpacing(10)

        # Поле пароля
        password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.login)

        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)
        main_layout.addSpacing(20)

        # Кнопка входа
        self.login_button = QPushButton('Войти')
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)

        main_layout.addSpacing(10)

        # Кнопка гостя
        self.guest_button = QPushButton('Войти как гость')
        self.guest_button.setMinimumHeight(40)
        self.guest_button.setStyleSheet('''
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        ''')
        self.guest_button.clicked.connect(self.login_as_guest)
        main_layout.addWidget(self.guest_button)

        self.setLayout(main_layout)

        # Центрирование окна
        self.center_window()

    def center_window(self):
        """Центрировать окно на экране"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def login(self):
        """Обработка входа в систему"""
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(
                self,
                'Ошибка',
                'Пожалуйста, заполните все поля!'
            )
            return

        try:
            user = UserQueries.authenticate(login, password)

            if user:
                self.current_user = user
                self.open_products_window()
            else:
                QMessageBox.warning(
                    self,
                    'Ошибка авторизации',
                    'Неверный логин или пароль!'
                )
                self.password_input.clear()

        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'Ошибка подключения к базе данных:\n{str(e)}'
            )

    def login_as_guest(self):
        """Вход как гость"""
        self.current_user = {
            'user_id': None,
            'full_name': 'Гость',
            'login': 'guest',
            'role_name': 'Гость'
        }
        self.open_products_window()

    def open_products_window(self):
        """Открыть окно списка товаров"""
        self.products_window = ProductsWindow(self.current_user, self)
        self.products_window.show()
        self.hide()

    def show_login(self):
        """Показать окно авторизации (при выходе)"""
        self.login_input.clear()
        self.password_input.clear()
        self.show()
