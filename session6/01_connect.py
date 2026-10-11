# Урок 9, шаг 1 (слайд 6): подключиться к PostgreSQL из Python.
#
# Один раз перед первым запуском, в терминале VS Code:
#     python -m pip install psycopg2-binary matplotlib
#
# Запуск из папки session6:
#     python 01_connect.py
#
# Чем отличается от слайда:
# - база postgres и пароль postgres, как на компьютерах в классе. База
#   postgres есть на любом PostgreSQL сразу после установки, создавать её
#   не надо. На слайде база test2 и пароль 1111: это настройки автора
#   урока, у нас таких нет.
# - на слайде есть строка "from psycopg2 import sql". В уроке она нигде
#   не нужна, поэтому её здесь нет.
# - на слайде программа ничего не печатает. Здесь в конце print, чтобы
#   было видно, что подключение получилось.

import psycopg2

# Подключение к PostgreSQL, к служебной базе postgres: она есть всегда.
# Это те же ответы, что SQL Shell спрашивает при входе:
# сервер, база, порт, пользователь, пароль.
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)

# autocommit = True: каждая команда сразу сохраняется в базе.
# На следующем шаге без этой строки базу не создать.
connection.autocommit = True

# cursor (курсор): через него отправляют команды базе и забирают ответы.
cursor = connection.cursor()

print("Подключение к базе postgres есть")

cursor.close()
connection.close()
