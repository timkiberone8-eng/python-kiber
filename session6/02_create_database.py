# Урок 9, шаг 2 (слайд 7): создать из Python новую базу sales_data.
#
# Запуск из папки session6:
#     python 02_create_database.py
#
# Подключаемся к служебной базе postgres (как в шаге 1), а оттуда создаём
# отдельную базу sales_data: в ней будут продажи. Отличия от слайда те же,
# что в шаге 1: база postgres и пароль postgres вместо test2 и 1111.
#
# Запускать можно сколько угодно раз: DROP DATABASE IF EXISTS сначала
# удаляет старую sales_data. Но вместе с ней пропадают таблица и продажи,
# поэтому после этого шага снова запусти шаги 3 и 4.

import psycopg2

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)

# Без этой строки CREATE DATABASE не сработает. Подробности в README.
connection.autocommit = True
cursor = connection.cursor()

# Создание базы данных.
# DROP DATABASE IF EXISTS: удалить базу, если она есть, а если нет,
# ничего не делать и не ругаться.
cursor.execute("DROP DATABASE IF EXISTS sales_data")
cursor.execute("CREATE DATABASE sales_data")
print("База данных создана")

# Закрываем текущее подключение
cursor.close()
connection.close()
