# ШАГ 2. Передаём те же товары в HTML-шаблон
# ОТКРЫТЬ: catalog/views.py — приложение рядом с manage.py.
# ДЕЙСТВИЕ: добавьте render и замените только home. Остальные функции сохраните.

from django.shortcuts import render

from .models import Product


def home(request):
    products = Product.objects.filter(price__lte=100).order_by('price', 'id')
    # Шаблон получает выборку под именем products для цикла {% for %}.
    return render(request, 'catalog/product_list.html', {'products': products})

# ПРОВЕРКА: на главной появился HTML-каталог, состав и порядок товаров прежние.
