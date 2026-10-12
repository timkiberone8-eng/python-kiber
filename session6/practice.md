---
layout: default
title: "Закрепление занятия 6: Python и база данных"
---

# Закрепление занятия 6: Python и база данных

Здесь программы с занятия с пояснениями, объяснение, что такое курсор и зачем `commit`, шесть ошибок, которые случались на занятии, и задачи на новой базе с проверкой.

Объяснения спрятаны под строками «Подробнее»: открывай, если что-то непонятно.

## 0. Что нужно дома

1. **PostgreSQL** с паролем `postgres` у пользователя `postgres`, как в классе. Как поставить, написано в [конспекте занятия 5](../zanyatie5/konspekt.html), раздел «1. Вход».
2. **psycopg2.** Один раз, в терминале VS Code:

   ```bash
   python -m pip install psycopg2-binary
   ```

   Проверка: `python -c "import psycopg2; print(psycopg2.__version__)"` печатает номер версии, например `2.9.13 (dt dec pq3 ext lo64)`.
3. **База `sales_data` с продажами.** Она нужна для программ с занятия и ошибок, задачам не нужна. Если её у тебя нет, запусти по очереди шаги 2, 3 и 4 из [учебника](https://github.com/timkiberone8-eng/python-kiber/tree/main/session6): `02_create_database.py`, `03_create_table.py`, `04_insert_data.py`.

Запускай программы в терминале VS Code: `python имя_файла.py`.

## 1. Программы с занятия

Две программы с занятия: первая записывает продажи в таблицу `sales` (шаг 4), вторая спрашивает у базы выручку по каждому продукту (шаг 5).

### Записать данные

```python
import psycopg2
from datetime import datetime

# подключение: те же ответы, что SQL Shell спрашивает при входе
connection = psycopg2.connect(
    database="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
# курсор: через него отправляем команды и забираем ответы
cursor = connection.cursor()

# стереть продажи прошлого запуска, чтобы не записать их дважды
cursor.execute("DELETE FROM sales")

# список продаж: каждая продажа это кортеж (товар, штук, цена, дата)
sales_data = [
    ("Laptop", 10, 700, datetime(2024, 1, 10)),
    ("Smartphone", 25, 300, datetime(2024, 1, 11)),
    ("Tablet", 15, 250, datetime(2024, 1, 12)),
    ("Headphones", 50, 50, datetime(2024, 1, 13)),
    ("Smartwatch", 30, 150, datetime(2024, 1, 14)),
]

# %s: место для значения, psycopg2 подставит туда значения из sale по порядку
for sale in sales_data:
    cursor.execute("INSERT INTO sales (product_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)", sale)

# сохранить всё, что записали; без этой строки в базе ничего не останется
connection.commit()
print("Данные добавлены")

# закрыть курсор и подключение
cursor.close()
connection.close()
```

**Что такое `sale`.** `sales_data` это список из пяти продаж, каждая продажа записана кортежем: четыре значения в круглых скобках. `for sale in sales_data:` проходит по списку, и на каждом круге в переменной `sale` лежит одна продажа: на первом круге `("Laptop", 10, 700, datetime(2024, 1, 10))`, на втором продажа Smartphone и так далее. Кругов пять, значит пять команд `INSERT`.

Вторым аргументом `execute` получает `sale`, то есть четыре значения. psycopg2 раскладывает их по четырём `%s` по порядку. Тексту он сам ставит кавычки, дату переводит в понятный базе вид.

<details markdown="1">
<summary markdown="span">Подробнее: увидеть, что лежит в sale и что уходит в базу</summary>

Сделай копию программы «Записать данные», убери из копии строку с `DELETE` (иначе она сотрёт продажи) и замени цикл на такой. В нём два `print`, а вместо `execute` стоит `mogrify`: он собирает команду так же, как `execute`, но не отправляет её в базу, а только возвращает. На занятии его не было, здесь он нужен, только чтобы заглянуть внутрь.

```python
for sale in sales_data:
    print(sale)
    print(cursor.mogrify("INSERT INTO sales (product_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)", sale).decode())
```

После запуска программа напечатает вот это (здесь только первые две продажи, остальные три выглядят так же; в конце, как и раньше, «Данные добавлены», хотя в базу ничего не ушло: этот `print` просто печатает текст):

```
('Laptop', 10, 700, datetime.datetime(2024, 1, 10, 0, 0))
INSERT INTO sales (product_name, quantity, price, sale_date) VALUES ('Laptop', 10, 700, '2024-01-10T00:00:00'::timestamp)
('Smartphone', 25, 300, datetime.datetime(2024, 1, 11, 0, 0))
INSERT INTO sales (product_name, quantity, price, sale_date) VALUES ('Smartphone', 25, 300, '2024-01-11T00:00:00'::timestamp)
```

У `Laptop` появились кавычки, числа остались без них. Дата стала текстом `'2024-01-10T00:00:00'` с пометкой `::timestamp` («это дата и время»), а столбец `DATE` время отбросит. `.decode()` нужен, потому что `mogrify` возвращает команду байтами, а `decode` делает из них обычную строку.

</details>

### Спросить у базы

```python
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

# забрать ответ базы целиком: список строк, каждая строка это кортеж
revenue_data = cursor.fetchall()
for row in revenue_data:
    print(f"Продукт: {row[0]}, Общая выручка: {row[1]}")

cursor.close()
connection.close()
```

Печатает:

```
Продукт: Smartphone, Общая выручка: 7500
Продукт: Laptop, Общая выручка: 7000
Продукт: Smartwatch, Общая выручка: 4500
Продукт: Tablet, Общая выручка: 3750
Продукт: Headphones, Общая выручка: 2500
```

Три тройных кавычки `"""` нужны, чтобы написать команду SQL в несколько строк: так её легче читать. Базе всё равно, в одну строку команда или в пять.

### Запрос с GROUP BY по строкам

| Строка | Что делает |
|---|---|
| `SELECT product_name, ...` | что показать: название продукта и ещё один столбец |
| `SUM(quantity * price)` | для каждой продажи умножить штуки на цену (это выручка одной продажи) и сложить внутри группы |
| `AS total_revenue` | дать этому столбцу имя, чтобы ниже на него сослаться |
| `FROM sales` | из какой таблицы |
| `GROUP BY product_name` | собрать строки с одинаковым продуктом в одну группу: сколько разных продуктов, столько строк в ответе |
| `ORDER BY total_revenue DESC` | отсортировать по выручке, `DESC` значит от большего к меньшему |

Проверь одну строку сам: Smartphone 25 штук по 300, это 7500.

<details markdown="1">
<summary markdown="span">Подробнее: зачем GROUP BY, если каждый продукт продан один раз</summary>

В наших пяти продажах каждый продукт встречается один раз, поэтому в каждой группе одна строка и сложение ничего не меняет. GROUP BY видно, когда у продукта несколько продаж: тогда несколько строк сворачиваются в одну, а `SUM` складывает их. Так будет в задачах ниже, на новой базе: там Minecraft купили три раза.

Порядок частей запроса строгий: `SELECT`, `FROM`, `GROUP BY`, `ORDER BY`. Поменяешь местами, база ответит ошибкой синтаксиса.

</details>

## 2. Курсор

Подключение (`connection`) это открытый разговор с базой: ты вошёл на сервер под своим пользователем в нужную базу, как в SQL Shell. Курсор (`cursor`) это то, через что в этом разговоре идут команды и ответы:

- `cursor.execute("...")` отправляет базе команду;
- ответ база кладёт в курсор, и он лежит там, пока ты его не заберёшь;
- `cursor.fetchall()` забирает ответ.

Поэтому `execute` сам ничего не возвращает. Если написать `answer = cursor.execute("SELECT ...")`, в `answer` окажется `None`, а ответ останется в курсоре.

В SQL Shell курсор не нужен: там ответ сразу печатается на экран, и читаешь его ты. В программе ответ читает сама программа, и ей нужно место, откуда его взять.

<details markdown="1">
<summary markdown="span">Подробнее: почему он называется курсором</summary>

Cursor по-английски «указатель». Как курсор в тексте показывает, где ты сейчас, курсор базы помнит, до какой строки ответа ты уже дочитал. Это видно, если забирать ответ по одной строке: для этого есть `fetchone()`. На занятии его не было, здесь он нужен, только чтобы увидеть, как работает курсор:

```python
import psycopg2

connection = psycopg2.connect(
    database="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

answer = cursor.execute("SELECT product_name, quantity FROM sales ORDER BY id")
print("execute вернул:", answer)

print("fetchone:", cursor.fetchone())
print("fetchone:", cursor.fetchone())
print("fetchall:", cursor.fetchall())
print("fetchall ещё раз:", cursor.fetchall())

cursor.close()
connection.close()
```

```
execute вернул: None
fetchone: ('Laptop', 10)
fetchone: ('Smartphone', 25)
fetchall: [('Tablet', 15), ('Headphones', 50), ('Smartwatch', 30)]
fetchall ещё раз: []
```

- `execute` вернул `None`: ответ лёг в курсор.
- `fetchone` взял первую строку и передвинул указатель на вторую, следующий `fetchone` взял вторую.
- `fetchall` забрал **оставшиеся** строки, а не все: указатель уже стоял на третьей.
- Второй `fetchall` вернул пустой список: указатель в конце ответа, забирать нечего. Чтобы получить ответ заново, нужен новый `execute`.

</details>

## 3. Транзакция, commit и autocommit

**Транзакция** это пачка команд, которая сохраняется в базе целиком или не сохраняется вовсе. Пример, ради которого её придумали: перевод денег. Списать 100 рублей с одного счёта и зачислить на другой это две команды. Если программа упадёт между ними, деньги не должны пропасть: база отменит и списание.

Как это устроено в psycopg2:

1. Перед первой командой psycopg2 сам, молча, начинает транзакцию.
2. Всё, что ты дальше делаешь через этот `connection`, идёт внутри неё: изменения видны только твоей программе, в базе их ещё нет.
3. `connection.commit()` сохраняет транзакцию, и изменения попадают в базу.
4. Закрыл подключение без `commit` или программа упала с ошибкой: транзакция отменяется, всё, что ты в ней сделал, пропадает.

Поэтому `commit` нужен после всего, что **меняет** базу: `CREATE TABLE`, `INSERT`, `UPDATE`, `DELETE`. После `SELECT` он не нужен: `SELECT` ничего не меняет, сохранять нечего.

<details markdown="1">
<summary markdown="span">Подробнее: что будет без commit</summary>

В таблице `sales` пять продаж. Записываем шестую и не сохраняем:

```python
import psycopg2
from datetime import datetime

connection = psycopg2.connect(
    database="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("INSERT INTO sales (product_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)",
               ("Mouse", 5, 20, datetime(2024, 1, 15)))
print("Добавлено")

cursor.close()
connection.close()
```

Программа печатает `Добавлено` и заканчивается без ошибок. А `SELECT COUNT(*) FROM sales` (сколько строк в таблице) после неё отвечает `5`: мышки в базе нет. `print` просто печатает текст, он не знает, сохранилось что-то или нет.

</details>

<details markdown="1">
<summary markdown="span">Подробнее: ошибка посередине, «всё или ничего»</summary>

Записываем три продажи, в третьей вместо числа штук слово:

```python
import psycopg2
from datetime import datetime

connection = psycopg2.connect(
    database="sales_data",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

new_sales = [
    ("Mouse", 5, 20, datetime(2024, 1, 15)),
    ("Keyboard", 3, 40, datetime(2024, 1, 16)),
    ("Monitor", "много", 200, datetime(2024, 1, 17)),
]
for sale in new_sales:
    cursor.execute("INSERT INTO sales (product_name, quantity, price, sale_date) VALUES (%s, %s, %s, %s)", sale)
    print("Добавлено:", sale[0])

connection.commit()
cursor.close()
connection.close()
```

```
Добавлено: Mouse
Добавлено: Keyboard
Traceback (most recent call last):
  ...
psycopg2.errors.InvalidTextRepresentation: ОШИБКА:  неверный синтаксис для типа integer: "много"
```

Две продажи «добавлены», но до `commit` программа не дошла. В таблице по-прежнему 5 строк: не сохранились ни мышка, ни клавиатура. Пачка не сохранилась целиком, половины записей в базе нет. Исправил данные, запустил заново, и всё запишется один раз.

</details>

**autocommit.** Если написать `connection.autocommit = True`, транзакций нет: каждая команда сохраняется в базе сразу, как только выполнилась, `commit` не нужен.

Тогда зачем вообще `commit`? Затем, что с `autocommit` нет «всё или ничего». Та же программа с тремя продажами, только с `autocommit`, печатает то же самое и падает на той же строке, но в таблице после неё уже 7 строк: мышка и клавиатура сохранились, монитор нет. Запустишь исправленную программу ещё раз, и мышка с клавиатурой запишутся второй раз.

**Почему на занятии в шагах 1 и 2 стоит `autocommit`, а в шагах 3 и 4 `commit`.** Создавать и удалять базу PostgreSQL внутри транзакции не разрешает. Без `autocommit` шаг 2 падает так:

```
psycopg2.errors.ActiveSqlTransaction: ОШИБКА:  DROP DATABASE не может выполняться внутри блока транзакции
```

А таблицу и данные выгоднее записывать транзакцией: упало посередине, и в базе не останется половины.

<details markdown="1">
<summary markdown="span">Подробнее: почему в SQL Shell на занятии 5 commit не писали</summary>

В SQL Shell autocommit включён сразу: каждая команда сохраняется, как только ты нажал Enter. Поэтому `INSERT` там сохранялся без всякого `commit`. psycopg2 устроен наоборот: по умолчанию autocommit выключен, и сохраняет только `commit`.

</details>

## 4. Найди ошибку

Такие ошибки были на занятии. Сначала подумай, что не так, потом открывай ответ. Все программы ниже это программы из раздела 1 с одной ошибкой, поэтому их можно запустить и посмотреть на ответ Python сам.

**Ошибка 1.** Программа «Спросить у базы», только в подключении стоит:

```python
    database="postgres",
```

```
psycopg2.errors.UndefinedTable: ОШИБКА:  отношение "sales" не существует
LINE 3: FROM sales
             ^
```

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

Подключились не к той базе. Таблица `sales` живёт в базе `sales_data`, а в служебной базе `postgres` её нет. «Отношение» это таблица, так PostgreSQL называет её в ошибках. Нужно `database="sales_data"`.

К `postgres` подключались только в шагах 1 и 2: оттуда создают новую базу. Всё, что дальше, в `sales_data`. Если копируешь начало программы из шага 1 или 2, поправь имя базы.

</details>

**Ошибка 2.**

```python
SELECT product_name, SUM(quntity * price) AS total_revenue
```

```
psycopg2.errors.UndefinedColumn: ОШИБКА:  столбец "quntity" не существует
LINE 2: SELECT product_name, SUM(quntity * price) AS total_revenue
                                 ^
HINT:  Возможно, предполагалась ссылка на столбец "sales.quantity".
```

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

Опечатка: `quntity` вместо `quantity`. Галочка `^` под строкой показывает место, а строка `HINT` (подсказка) даже называет правильный столбец. Читай ошибку до конца: часто ответ в ней уже есть.

Если столбец назван иначе при создании таблицы (`sales_date` вместо `sale_date`), запросы с другим именем тоже будут падать этой ошибкой. Как называются столбцы, видно в шаге 3 или в SQL Shell: `\d sales`.

</details>

**Ошибка 3.**

```python
cursor.execute("""
SELECT product_name, SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
""")

cursor.fetchall()
for row in revenue_data:
    print(f"Продукт: {row[0]}, Общая выручка: {row[1]}")
```

```
NameError: name 'revenue_data' is not defined
```

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

`fetchall()` забрал ответ, но его никуда не положили, и он пропал. А переменной `revenue_data` нигде не присвоено значение, поэтому Python о ней не знает. Нужно `revenue_data = cursor.fetchall()`.

Это ошибка Python, а не базы: запрос к базе прошёл, сломалось то, что после него.

</details>

**Ошибка 4.**

```python
sales_data = [
    ("Laptop", 10, 700, datetime(2024, 1, 10)),
    ("Smartphone", 25, 300, datetime(2024, 1, 11))
    ("Tablet", 15, 250, datetime(2024, 1, 12)),
    ("Headphones", 50, 50, datetime(2024, 1, 13)),
    ("Smartwatch", 30, 150, datetime(2024, 1, 14)),
]
```

```
SyntaxWarning: 'tuple' object is not callable; perhaps you missed a comma?
...
TypeError: 'tuple' object is not callable
```

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

После кортежа со Smartphone нет запятой. Без неё Python читает `(...)(...)` как вызов: «возьми кортеж и вызови его, как функцию, со скобками после него». Кортеж это не функция, его нельзя вызвать: `'tuple' object is not callable`. Python даже подсказывает: `perhaps you missed a comma?`, «возможно, ты пропустил запятую?».

Запятая нужна после каждого элемента списка. После последнего её можно ставить или не ставить, обе записи верны.

</details>

**Ошибка 5.** Программа «Записать данные» без строки `connection.commit()`. Таблицу перед этим создали заново (шаги 2 и 3).

```
Данные добавлены
```

Ошибки нет, но `SELECT COUNT(*) FROM sales` отвечает `0`.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

Без `commit` транзакция при закрытии подключения отменилась, и записанное пропало (раздел 3). `print("Данные добавлены")` всё равно напечатал свой текст: он не проверяет, что в базе.

</details>

**Ошибка 6.**

```python
execute("""
SELECT product_name, SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
""")
```

```
NameError: name 'execute' is not defined
```

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

`execute` это не отдельная функция, а умение курсора. Пишется через точку: `cursor.execute(...)`. Так же `cursor.fetchall()`, `connection.commit()`, `cursor.close()`: слева от точки тот, кто делает, справа что он делает.

</details>

## 5. Задачи

Задачи на новой базе: магазин игр, таблица покупок. Программы пиши сами, каждую в своём файле. Подглядывать в раздел 1 можно: начало у всех программ одинаковое, меняется запрос.

### Задача 1. Новая база

Напиши программу, которая создаёт базу `game_shop`.

**Проверь себя:** программа печатает твоё сообщение и заканчивается без ошибки. Второй запуск тоже без ошибки.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
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

cursor.execute("DROP DATABASE IF EXISTS game_shop")
cursor.execute("CREATE DATABASE game_shop")
print("База game_shop создана")

cursor.close()
connection.close()
```

Подключаемся к `postgres`, потому что `game_shop` ещё нет. `autocommit` нужен: базу внутри транзакции не создать. `DROP DATABASE IF EXISTS` сначала удаляет старую `game_shop`, поэтому второй запуск не падает.

</details>

### Задача 2. Таблица и покупки

Напиши программу, которая в базе `game_shop` создаёт таблицу `purchases` (покупки) и записывает в неё покупки из списка. Столбцы:

| Столбец | Тип | Что в нём |
|---|---|---|
| `id` | `SERIAL PRIMARY KEY` | номер покупки, ставит база |
| `game` | `VARCHAR(100)` | название игры |
| `quantity` | `INT` | сколько штук купили |
| `price` | `DECIMAL` | цена одной штуки |
| `purchase_date` | `DATE` | дата покупки |

Список покупок можно скопировать, кнопка «Копировать» в правом верхнем углу:

<div class="copyable" markdown="1">

```python
purchases = [
    ("Minecraft", 2, 1500, datetime(2024, 3, 1)),
    ("Terraria", 1, 500, datetime(2024, 3, 1)),
    ("Minecraft", 2, 1500, datetime(2024, 3, 2)),
    ("Hollow Knight", 3, 600, datetime(2024, 3, 2)),
    ("Terraria", 6, 500, datetime(2024, 3, 3)),
    ("Stardew Valley", 2, 700, datetime(2024, 3, 3)),
    ("Minecraft", 1, 1500, datetime(2024, 3, 4)),
    ("Hollow Knight", 1, 600, datetime(2024, 3, 5)),
]
```

</div>

Остальное набирай сам. Чтобы программу можно было запускать несколько раз, перед записью сотри старые покупки, как в разделе 1.

**Проверь себя:** программа печатает твоё сообщение без ошибки. Есть ли покупки в базе на самом деле, проверит задача 3.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
import psycopg2
from datetime import datetime

connection = psycopg2.connect(
    database="game_shop",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    game VARCHAR(100),
    quantity INT,
    price DECIMAL,
    purchase_date DATE
)
""")
cursor.execute("DELETE FROM purchases")

purchases = [
    ("Minecraft", 2, 1500, datetime(2024, 3, 1)),
    ("Terraria", 1, 500, datetime(2024, 3, 1)),
    ("Minecraft", 2, 1500, datetime(2024, 3, 2)),
    ("Hollow Knight", 3, 600, datetime(2024, 3, 2)),
    ("Terraria", 6, 500, datetime(2024, 3, 3)),
    ("Stardew Valley", 2, 700, datetime(2024, 3, 3)),
    ("Minecraft", 1, 1500, datetime(2024, 3, 4)),
    ("Hollow Knight", 1, 600, datetime(2024, 3, 5)),
]
for purchase in purchases:
    cursor.execute("INSERT INTO purchases (game, quantity, price, purchase_date) VALUES (%s, %s, %s, %s)", purchase)

connection.commit()
print("Покупки записаны")

cursor.close()
connection.close()
```

`IF NOT EXISTS`: создать таблицу, только если её ещё нет, иначе второй запуск упадёт с ошибкой «отношение "purchases" уже существует». В одной транзакции тут и таблица, и покупки, поэтому `commit` один, в конце.

</details>

### Задача 3. Все покупки

Выведи все покупки, каждую на своей строке, по порядку номеров.

**Проверь себя:** 8 строк, первая Minecraft 2 штуки 1 марта, последняя Hollow Knight 1 штука 5 марта.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
import psycopg2

connection = psycopg2.connect(
    database="game_shop",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("SELECT * FROM purchases ORDER BY id")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
connection.close()
```

После первого запуска задачи 2 печатает:

```
(1, 'Minecraft', 2, Decimal('1500'), datetime.date(2024, 3, 1))
(2, 'Terraria', 1, Decimal('500'), datetime.date(2024, 3, 1))
(3, 'Minecraft', 2, Decimal('1500'), datetime.date(2024, 3, 2))
(4, 'Hollow Knight', 3, Decimal('600'), datetime.date(2024, 3, 2))
(5, 'Terraria', 6, Decimal('500'), datetime.date(2024, 3, 3))
(6, 'Stardew Valley', 2, Decimal('700'), datetime.date(2024, 3, 3))
(7, 'Minecraft', 1, Decimal('1500'), datetime.date(2024, 3, 4))
(8, 'Hollow Knight', 1, Decimal('600'), datetime.date(2024, 3, 5))
```

- `Decimal('1500')` это точное число из столбца `DECIMAL`, так Python показывает его, когда печатаешь кортеж целиком. В f-строке оно печатается просто `1500`.
- `datetime.date(2024, 3, 1)` это дата из столбца `DATE`, без времени.
- Запускал задачу 2 несколько раз, и номера начинаются не с 1, а, например, с 9? Это нормально: `DELETE` стирает строки, но счётчик `SERIAL` не сбрасывает, он выдаёт следующие номера.

</details>

### Задача 4. Выручка по играм

Выведи для каждой игры, сколько денег она принесла, самая прибыльная сверху.

**Проверь себя:** 4 строки, первая Minecraft 7500, последняя Stardew Valley 1400.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
import psycopg2

connection = psycopg2.connect(
    database="game_shop",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("""
SELECT game, SUM(quantity * price) AS total_revenue
FROM purchases
GROUP BY game
ORDER BY total_revenue DESC
""")
for row in cursor.fetchall():
    print(f"Игра: {row[0]}, выручка: {row[1]}")

cursor.close()
connection.close()
```

```
Игра: Minecraft, выручка: 7500
Игра: Terraria, выручка: 3500
Игра: Hollow Knight, выручка: 2400
Игра: Stardew Valley, выручка: 1400
```

Здесь GROUP BY уже работает: три покупки Minecraft (2, 2 и 1 штука по 1500) свернулись в одну строку, 3000 + 3000 + 1500 = 7500.

</details>

### Задача 5. Сколько штук

Выведи для каждой игры, сколько штук продано всего, больше всего сверху. Сравни с задачей 4: первая игра та же?

**Проверь себя:** первая строка Terraria 7, вторая Minecraft 5.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
import psycopg2

connection = psycopg2.connect(
    database="game_shop",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("""
SELECT game, SUM(quantity) AS total_quantity
FROM purchases
GROUP BY game
ORDER BY total_quantity DESC
""")
for row in cursor.fetchall():
    print(f"Игра: {row[0]}, продано штук: {row[1]}")

cursor.close()
connection.close()
```

```
Игра: Terraria, продано штук: 7
Игра: Minecraft, продано штук: 5
Игра: Hollow Knight, продано штук: 4
Игра: Stardew Valley, продано штук: 2
```

Штук больше всего у Terraria, а денег больше всего принёс Minecraft: он дороже. Поэтому «самый продаваемый» и «самый прибыльный» это разные вопросы, и запросы к базе у них разные.

</details>

### Задача 6. Покупки одной игры

Программа спрашивает название игры (`input`) и выводит все её покупки: дату, сколько штук, цену. В конце число покупок.

Подсказка: в `WHERE` значение подставь через `%s`, как в `INSERT` в разделе 1. Отбор с `WHERE` был на занятии 5.

**Проверь себя:** на `Minecraft` три покупки, 1, 2 и 4 марта. На `minecraft` с маленькой буквы ноль: для базы это разные слова.

<details markdown="1">
<summary markdown="span">Показать ответ</summary>

```python
import psycopg2

connection = psycopg2.connect(
    database="game_shop",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

game = input("Какая игра? ")
cursor.execute("SELECT purchase_date, quantity, price FROM purchases WHERE game = %s ORDER BY purchase_date", (game,))
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]} шт. по {row[2]}")
print("Покупок:", len(rows))

cursor.close()
connection.close()
```

```
Какая игра? Minecraft
2024-03-01: 2 шт. по 1500
2024-03-02: 2 шт. по 1500
2024-03-04: 1 шт. по 1500
Покупок: 3
```

Значения для `%s` передаются кортежем, даже если значение одно. Кортеж из одного элемента пишется с запятой: `(game,)`. Без запятой `(game)` это просто `game` в скобках, строка, а не кортеж, и psycopg2 падает:

```
TypeError: not all arguments converted during string formatting
```

</details>

<details markdown="1">
<summary markdown="span">Подробнее: почему не f-строка</summary>

Кажется, проще так: `cursor.execute(f"SELECT ... WHERE game = '{game}'")`. Но если в названии есть апостроф, например `Kid's Tablet`, кавычка из названия закроет кавычку в запросе раньше времени:

```
psycopg2.errors.SyntaxError: ОШИБКА:  ошибка синтаксиса (примерное положение: "s")
LINE 1: SELECT * FROM sales WHERE product_name = 'Kid's Tablet'
```

С `%s` psycopg2 сам расставляет кавычки и правильно обрабатывает такие символы: в базу уходит `'Kid''s Tablet'`, две кавычки подряд для базы значат одну кавычку внутри текста. Есть и причина серьёзнее: через f-строку злоумышленник может вписать в поле ввода свою команду SQL, и база её выполнит. Поэтому значения в запросы подставляют только через `%s`.

</details>

Захочешь пройти задачи заново: запусти задачу 1, она создаст базу `game_shop` с нуля.
