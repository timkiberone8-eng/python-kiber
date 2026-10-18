# Уроки 11-12, шаг 5 (слайды 20-22): Django хранит данные в PostgreSQL.
#
# Это не отдельная программа, а кусок файла mysite/mysite/settings.py.
# Запускать его не надо.
#
# 1. Создай базу blog_db. В SQL Shell (psql) после входа:
#        CREATE DATABASE blog_db;
#    Ответ: CREATE DATABASE
# 2. Открой mysite/mysite/settings.py, найди кусок DATABASES = { ... }
#    (строки 75-80) и замени его целиком на текст ниже. Сохрани (Ctrl+S).
# 3. В терминале, в папке mysite (там, где manage.py):
#        python manage.py migrate
#    Django создаст в blog_db свои таблицы. Последняя строка ответа:
#        Applying sessions.0001_initial... OK
#
# Чем отличается от слайдов:
# - на слайде 20 ставят pip install psycopg2. У тебя он уже стоит с урока 9
#   (пакет psycopg2-binary), ставить ничего не надо.
# - на слайде 21 'USER': 'potsrges', это опечатка: имя пользователя postgres.
# - на слайде 21 'PASSWORD': 'your_password', у нас пароль postgres.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',       # имя базы
        'USER': 'postgres',      # пользователь PostgreSQL
        'PASSWORD': 'postgres',  # его пароль
        'HOST': '127.0.0.1',     # сервер: этот компьютер
        'PORT': '5432',          # порт PostgreSQL
    }
}
