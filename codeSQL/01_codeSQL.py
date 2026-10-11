import psycopg2
connection = psycopg2.connect(
    dbname="postgres",
    user="postgers",
    password="postgres",
    host = "127.0.0.1",
    port = "5432"
)

connection.autocommit =True

cursor = connection.cursor()

print("подключение к базе есть")

cursor.close()
connection.close()
