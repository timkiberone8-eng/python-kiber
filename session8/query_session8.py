import psycopg2

DB_NAME = "sales_data"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host="127.0.0.1", port=5432
)
cursor = connection.cursor()

cursor.execute("""
SELECT product_name, COUNT(*) AS purchases, SUM(quantity) AS units, SUM(quantity * price) AS revenue
FROM lesson8_receipts
GROUP BY product_name
""")
result = cursor.fetchall()

cursor.close()
connection.close()

for row in result:
    print(row[3])
