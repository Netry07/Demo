import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from views.login_window import LoginWindow
from database.connection import db


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #FFFFFF;
        color: #000000;
    }
    QLineEdit, QTextEdit, QPlainTextEdit,
    QComboBox, QSpinBox, QDoubleSpinBox {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #CCCCCC;
        border-radius: 3px;
        padding: 3px;
    }
    QComboBox QAbstractItemView {
        background-color: #FFFFFF;
        color: #000000;
        selection-background-color: #E0FFE0;
        selection-color: #000000;
    }
""")
    app.setApplicationName('Магазин обуви')
    app.setOrganizationName('ShoeStore')

    # Установка иконки приложения
    try:
        app.setWindowIcon(QIcon('resources/images/icon.ico'))
    except:
        pass

    # Применение глобальных стилей

    # Проверка подключения к базе данных
    try:
        db.connect()
        print('Приложение успешно запущено')
        print('Подключение к базе данных установлено')
    except Exception as e:
        QMessageBox.critical(
            None,
            'Ошибка подключения',
            f'Не удалось подключиться к базе данных!\n\n'
            f'Ошибка: {str(e)}\n\n'
            f'Проверьте:\n'
            f'1. PostgreSQL запущен\n'
            f'2. База данных "shop" существует\n'
            f'3. Логин и пароль в файле config.ini правильные\n'
            f'(если файла нет, скопируйте config.ini.example в config.ini)'
        )
        sys.exit(1)

    login_window = LoginWindow()
    login_window.show()

    exit_code = app.exec()

    db.disconnect()
    print('Приложение завершено')

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
