# Дополнительно 2, срез по базам данных (урок 10), часть 1 (слайды 2-3):
# база company_data и в ней две таблицы, employees и sales.
#
# Запуск из папки session6:
#     python extra2_1_tables.py
#
# Запускать можно сколько угодно раз: каждый запуск создаёт базу
# company_data заново, пустой. После него снова extra2_2_data.py.

import psycopg2

# 1. Создать базу. Как в шаге 2 урока 9: подключаемся к postgres
# с autocommit и оттуда создаём новую базу.
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS company_data")
cursor.execute("CREATE DATABASE company_data")
cursor.close()
connection.close()
print("База company_data создана")

# 2. Подключиться к новой базе и создать таблицы
connection = psycopg2.connect(
    dbname="company_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

# Сотрудники. SERIAL PRIMARY KEY: номер ставится сам, по одному на строку
# (на слайде это названо «автоинкремент»).
cursor.execute("""
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    position VARCHAR(50),
    hire_date DATE
)
""")

# Продажи. REFERENCES employees(id) делает employee_id внешним ключом:
# в нём может стоять только такой номер, какой есть в столбце id
# таблицы employees. Продажу несуществующего сотрудника база не запишет.
# DECIMAL(10, 2): число с дробью, всего до 10 цифр, из них 2 после точки.
cursor.execute("""
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    product_name VARCHAR(100),
    quantity INTEGER,
    sale_amount DECIMAL(10, 2),
    sale_date DATE
)
""")

connection.commit()
print("Таблицы employees и sales созданы")

cursor.close()
connection.close()
