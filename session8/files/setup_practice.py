import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

purchases = [
    ("Сок", 2, 100, "2026-10-20"),
    ("Вода", 1, 20, "2026-10-20"),
    ("Сок", 1, 100, "2026-10-21"),
    ("Сэндвич", 3, 150, "2026-10-21"),
    ("Вода", 10, 20, "2026-10-22"),
    ("Сок", 1, 100, "2026-10-22"),
]

with psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
    host="127.0.0.1", port=5432
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lesson8_practice_receipts (
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                sale_date DATE NOT NULL
            )
        """)
        cursor.execute("DELETE FROM lesson8_practice_receipts")
        for purchase in purchases:
            cursor.execute("""
                INSERT INTO lesson8_practice_receipts
                    (product_name, quantity, price, sale_date)
                VALUES (%s, %s, %s, %s)
            """, purchase)
connection.close()
print("Готово: 6 покупок в таблице lesson8_practice_receipts.")
