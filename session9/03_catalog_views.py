# ШАГ 3. Главная страница
# ОТКРЫТЬ: catalog/views.py — папка catalog рядом с manage.py
# ДЕЙСТВИЕ: заменить содержимое; не создавать отдельный файл в mysite/mysite

from django.http import HttpResponse      # Ответ браузеру с HTML


def home(request):                       # Django передаст сюда запрос браузера
    return HttpResponse('<h1>Каталог работает</h1>')  # Возвращаем страницу

# ПРОВЕРКА: после следующего шага на / появится «Каталог работает»
