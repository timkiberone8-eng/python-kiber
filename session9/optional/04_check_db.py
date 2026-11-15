import getpass
import re

import psycopg2
from psycopg2 import sql

database = input('База PostgreSQL: ')
user = input('Пользователь PostgreSQL: ')
host = input('Сервер [127.0.0.1]: ') or '127.0.0.1'
port = input('Порт [5432]: ') or '5432'
schema = input('Своя новая схема, например catalog_example9: ')
if not re.fullmatch(r'catalog_[a-z0-9_]+', schema):
    raise ValueError('Имя схемы: catalog_ и далее маленькие латинские буквы, цифры, _')

connection = psycopg2.connect(
    dbname=database, user=user,
    password=getpass.getpass('Пароль PostgreSQL: '),
    host=host, port=port, connect_timeout=5,
)
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT current_database(), current_user')
            print(cursor.fetchone())
            cursor.execute('SELECT 1 FROM pg_namespace WHERE nspname = %s', (schema,))
            if cursor.fetchone():
                raise ValueError('Схема уже существует. Ничего не изменено. Для нового проекта выбери новое имя; для продолжения используй ранее проверенную свою схему.')
            cursor.execute(sql.SQL('CREATE SCHEMA {} AUTHORIZATION CURRENT_USER').format(sql.Identifier(schema)))
    print('Создана схема:', schema)
finally:
    connection.close()
