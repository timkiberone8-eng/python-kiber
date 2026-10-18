# Занятие 7: Django, первая страница сайта (уроки 11–12)

На уроке 9 Python спрашивал у базы итоги продаж, и ответ видел только ты, в своём терминале. Чтобы их увидел другой человек, нужна страница, которую он откроет по ссылке в браузере. Страницу браузеру отдаёт сервер: программа, которая ждёт запросов и на каждый отвечает страницей. Django это набор готовых деталей, из которых такой сервер собирается на Python.

Сегодня сервер работает на твоём компьютере, адрес `http://127.0.0.1:8000/`. `127.0.0.1` значит «этот компьютер»: страницу видишь только ты. Чтобы её открыл кто-то другой, сайт кладут на сервер в интернете; это позже.

## Чем отличается от слайдов

- На слайдах PyCharm. У нас VS Code: все команды набираешь в терминале VS Code.
- На слайде 8 `pip install django`, у нас `python -m pip install django`. На слайде 10 `django-admin startproject mysite`, у нас `python -m django startproject mysite`. Если папки Scripts нет в PATH (списке папок, где терминал ищет программы), терминал не найдёт ни `pip`, ни `django-admin`, а через `python -m` они запускаются всегда.
- На слайдах Django 5.1.3, у нас 6.1.2. Сервер при запуске пишет `Starting WSGI development server` вместо `Starting development server`, а в конце добавляет предупреждение `WARNING: This is a development server...`: это нормально, учебный сервер не для настоящего сайта.
- На слайде 17 список `urlpatterns` написан второй раз, целиком. Список нужен один: новую строку добавляй в старый (как в `03_urls_about.py`).
- На слайдах 18 и 19 в адресной строке `127.0.0.1:8000`, а надо `127.0.0.1:8000/about/` и `127.0.0.1:8000/contacts/`.
- На слайде 20 ставят `psycopg2`. Он у тебя уже стоит с урока 9 (пакет `psycopg2-binary`), ставить не надо.
- На слайде 21 `'USER': 'potsrges'` (опечатка, надо `postgres`) и `'PASSWORD': 'your_password'` (у нас `postgres`).

## 1. Установка (один раз)

В терминале VS Code:

```bash
python -m pip install django
```

Последняя строка установки:

```
Successfully installed asgiref-3.12.1 django-6.1.2 sqlparse-0.6.0 tzdata-2026.5
```

Если pip возьмёт версии новее, номера будут другие. Проверь, что встало:

```bash
python -m django --version
```

Ответ: номер версии, например `6.1.2`. Если вместо него `No module named django`, Django не установился, повтори установку.

## 2. Шаги

| Шаг | Слайды | Что сделать | Файл |
|---|---|---|---|
| 1 | 6–13 | создать проект `mysite` и запустить сервер | команды ниже |
| 2 | 14–16 | первая своя страница: `Hello, World!` | `02_urls_hello.py` |
| 3 | 17–18 | вторая страница по адресу `/about/` | `03_urls_about.py` |
| 4 | 19 | сам: своё имя на главной и страница `/contacts/` | ответ `answer_04_urls_name_contacts.py`, выложим после занятия |
| 5 | 20–22 | Django хранит данные в PostgreSQL | `05_settings_databases.py` |

Файлы шагов 2–4 это весь `urls.py` после шага: открой `mysite/mysite/urls.py` своего проекта, сотри всё и вставь текст файла. Шаг 5 это кусок `settings.py`. Сначала попробуй написать сам по слайду, потом сверься.

### Шаг 1: проект и сервер

В терминале VS Code перейди в папку, где лежат твои файлы урока 9, и создай проект:

```bash
python -m django startproject mysite
cd mysite
python manage.py runserver
```

`startproject` ничего не печатает, но рядом появляется папка `mysite`: в ней `manage.py` и ещё одна папка `mysite` с настройками (`settings.py`, `urls.py` и другие). `cd mysite` переходит в первую из них, туда, где `manage.py`.

Сервер пишет:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

а ниже дату, версию Django и адрес `http://127.0.0.1:8000/`. Строки про миграции это не ошибка: Django напоминает, что свои таблицы в базе он ещё не создал. Это шаг 5.

Открой в браузере `http://127.0.0.1:8000/`: ракета и надпись `The install worked successfully! Congratulations!`.

Пока сервер работает, терминал занят. Сервер сам замечает, когда ты сохраняешь файл проекта, и перезапускается: после правки достаточно обновить страницу в браузере. Остановить сервер: `Ctrl+C` в терминале. Если не останавливается, закрой терминал значком корзины.

### Шаги 2–4: страницы

После шага 2 на `http://127.0.0.1:8000/` будет `Hello, World!`. После шага 3 на `http://127.0.0.1:8000/about/` будет `Это страница о проекте.`. Адрес, где после `8000/` ничего нет (`127.0.0.1:8000/`), это главная страница, в `urlpatterns` она записана как `''`.

### Шаг 5: PostgreSQL

Что делать по порядку, написано в начале `05_settings_databases.py`: создать базу `blog_db` в SQL Shell, заменить кусок `DATABASES` в `settings.py`, запустить `python manage.py migrate` в папке, где `manage.py`. Сервер останавливать не надо: для `migrate` открой второй терминал (плюс в панели терминала) и перейди в ту же папку.

Порядок важен: сначала база, потом `settings.py`. Если сохранить `settings.py`, когда базы ещё нет, сервер в первом терминале упадёт с `UnicodeDecodeError` и страницы перестанут открываться. Тогда создай базу, запусти `migrate` и сохрани `settings.py` ещё раз (Ctrl+S): сервер запустится сам.

`migrate` пишет по строке на каждую таблицу Django и заканчивает так:

```
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

Второй раз `migrate` ответит `No migrations to apply.`: всё уже создано.

## 3. Если что-то пошло не так

| Что видишь | В чём дело | Что сделать |
|---|---|---|
| `No module named django` | Django не установлен в этот Python | `python -m pip install django` |
| `"django-admin" не распознано как имя командлета` (или по-английски `The term 'django-admin' is not recognized`) | терминал не нашёл `django-admin`: папки Scripts нет в PATH | `python -m django startproject mysite` |
| `can't open file '...manage.py': [Errno 2] No such file or directory` | ты не в папке проекта | `cd mysite`, потом снова `python manage.py runserver` |
| `CommandError: 'mysite' conflicts with the name of an existing Python module` | проект `mysite` здесь уже есть: ты запустил `startproject` второй раз | ничего не создавай заново: `cd mysite` |
| в браузере `Page not found (404)` | такого адреса в `urlpatterns` нет | сравни адрес в браузере со строками `path(...)`. `path('about/', about)` ловит адрес с косой чертой в конце: `/about/` |
| в браузере `NameError at /`, в терминале `NameError: name 'HttpResponse' is not defined` | нет строки `from django.http import HttpResponse` | добавь её наверх `urls.py` |
| в браузере `Не удается получить доступ к сайту`, в терминале `SyntaxError: expected ':'` | ошибка в `urls.py` (здесь нет двоеточия после `def hello(request)`), сервер не запустился | исправь и сохрани файл: сервер запустится сам |
| страница не меняется, хотя файл сохранён | возможно, в другом терминале работает ещё один сервер, и отвечает он | останови лишний сервер или закрой лишний терминал |
| `migrate` падает с `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2` | база не пустила: неверное имя пользователя или пароль, или базы `blog_db` нет. Как на уроке 9 | проверь `'USER': 'postgres'` и `'PASSWORD': 'postgres'`; создай базу `CREATE DATABASE blog_db;` |

Если ничего не помогло, сфотографируй экран с ошибкой и покажи на занятии.
