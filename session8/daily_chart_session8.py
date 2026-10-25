import psycopg2
import matplotlib.pyplot as plt

DB_NAME = "sales_data"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
    host="127.0.0.1", port=5432
)
cursor = connection.cursor()

cursor.execute("""
SELECT sale_date, SUM(price) AS revenue
FROM lesson8_receipts
GROUP BY sale_date
ORDER BY sale_date
""")
result = cursor.fetchall()

cursor.close()
connection.close()

dates = []
revenues = []

for row in result:
    dates.append(row[0])
    revenues.append(row[1])

plt.figure(figsize=(9, 5))
plt.plot(dates, revenues, marker="o")
plt.title("Выручка магазина по дням")
plt.xlabel("Дата")
plt.ylabel("Выручка, руб.")
plt.xticks(dates)
plt.tight_layout()
plt.show()
