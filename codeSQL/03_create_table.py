import psycopg2

connection = psycopg2.connect(
    dbname="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)

cursor = connection.cursor()

# Создание таблицы "sales" для хранения информации о продажах.
# IF NOT EXISTS: создать, только если такой таблицы ещё нет. Поэтому
# повторный запуск не падает с ошибкой «отношение "sales" уже существует».
# VARCHAR(100): текст не длиннее 100 символов.
# DECIMAL: точное число с дробью, для денег.
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL,
    sale_date DATE
)
""")

# Здесь autocommit нет, поэтому изменения надо сохранить самому.
# Без commit таблица не появится: при закрытии подключения всё,
# что не сохранено, отменяется.
connection.commit()
print("Таблица создана")

cursor.close()
connection.close() 