sales_data = [
    ("Laptop", 10, 700),
    ("Smartphone", 25, 300),
]

for sale in sales_data:
    name = sale[0]
    money = sale[1] * sale[2]
    print(name, money)

print("Готово")
