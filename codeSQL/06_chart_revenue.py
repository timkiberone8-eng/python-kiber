import psycopg2
import matplotlib.pyplot as plt

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


cursor.close()
connection.close()


products = [row[0] for row in revenue_data]
revenue = [row[1] for row in revenue_data]


plt.figure(figsize=(10, 6))
plt.bar(products, revenue, color="#8A2BE2", alpha=0.7)
plt.title("Общая выручка по продуктам")
plt.xlabel("Продукт")
plt.ylabel("Выручка")
plt.show()
