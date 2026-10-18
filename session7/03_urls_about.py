# Уроки 11-12, шаг 3 (слайды 17-18): вторая страница, /about/.
#
# Это весь файл mysite/mysite/urls.py после шага: к шагу 2 добавились
# функция about и строка path('about/', about).
# Сохрани и открой в браузере: http://127.0.0.1:8000/about/
#
# Что напечатает браузер:
#   на http://127.0.0.1:8000/        Hello, World!
#   на http://127.0.0.1:8000/about/  Это страница о проекте.
#
# Чем отличается от слайда:
# - на слайде 17 список urlpatterns написан второй раз, целиком, под
#   функцией about. Работает и так: второй список заменяет первый. Но
#   список нужен один, поэтому здесь новая строка добавлена в старый.
# - на слайде 18 в адресной строке видно 127.0.0.1:8000, а текст
#   «Это страница о проекте.». Адрес должен быть 127.0.0.1:8000/about/.

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello, World!")


def about(request):
    return HttpResponse("Это страница о проекте.")


urlpatterns = [
    path('', hello),
    path('about/', about),
]
