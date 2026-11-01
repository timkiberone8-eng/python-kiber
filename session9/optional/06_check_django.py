from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('SELECT current_database(), current_user, current_schema()')
    print(cursor.fetchone())
