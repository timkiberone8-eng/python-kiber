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

cursor.execute("DELETE FROM sells")
sells_data = [
    ("хлеб", 10, )
]
for sell 
cursor.close()
connection.close()
