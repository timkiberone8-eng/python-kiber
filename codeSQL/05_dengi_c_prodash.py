import psycopg2

connection = psycopg2.connect(
    database="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()


cursor.execute("""
SELECT product_name, SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
""")


revenue_data = cursor.fetchall()
for row in revenue_data:
    print(f"Продукт: {row[0]}, Общая выручка: {row[1]}")

cursor.close()
connection.close()
