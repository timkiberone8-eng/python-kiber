import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
    host="127.0.0.1", port=5432
)
cursor = connection.cursor()

cursor.execute("""
SELECT product_name, quantity, price, sale_date
FROM lesson8_practice_receipts
ORDER BY id
""")
result = cursor.fetchall()

cursor.close()
connection.close()

for row in result:
    print(row)
