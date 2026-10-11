import psycopg2

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute("DROP DATABASE IF EXISTS sales_data")
cursor.execute("CREATE DATABASE sales_data")
print("База данных создана")

cursor.close()
connection.close()