# ШАГ 1. Фильтр и сортировка в текстовом каталоге
# ОТКРЫТЬ: catalog/views.py — приложение рядом с manage.py.
# ДЕЙСТВИЕ: в готовой home замените только строку с Product.objects.all().

from django.http import HttpResponse

from .models import Product


def home(request):
    # lte означает «меньше или равно». Сортируем по цене, при равенстве — по id.
    products = Product.objects.filter(price__lte=100).order_by('price', 'id')
    lines = []

    for product in products:
        lines.append(f'{product.name} — {product.price} ₽')

    text = '\n'.join(lines) or 'Товаров пока нет'
    return HttpResponse(text, content_type='text/plain; charset=utf-8')

# ПРОВЕРКА: товар за 100 ₽ виден, товар дороже 100 ₽ остался в админке.
