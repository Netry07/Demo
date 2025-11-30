import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from views.login_window import LoginWindow
from database.connection import db


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Магазин обуви')
    app.setOrganizationName('ShoeStore')

    # Установка иконки приложения
    try:
        app.setWindowIcon(QIcon('resources/images/icon.ico'))
    except:
        pass

    # Применение глобальных стилей
    try:
        with open('resources/styles.qss', 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f'Не удалось загрузить стили: {e}')

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
            f'3. Логин и пароль в config.py правильные'
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
