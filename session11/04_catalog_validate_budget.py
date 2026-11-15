# ШАГ 4. Проверяем значение бюджета до преобразования в число
# ОТКРЫТЬ: catalog/views.py — приложение рядом с manage.py.
# ДЕЙСТВИЕ: после проверки шага 3 замените только home.
#
# На шаге 3 int("abc") останавливает выполнение. Здесь до int() проверяем
# содержимое адреса и даём покупателю подсказку, если ввели что-то другое.

from django.shortcuts import render

from .models import Product


def home(request):
    # Поле с name="max_price" передаёт сумму в адресе. Например, /?max_price=60.
    # request.GET отдаёт текст. Если суммы в адресе нет, получаем пустую строку.
    max_price = request.GET.get('max_price', '').strip()
    error = ''

    # При пустом поле показываем весь каталог, в порядке от дешёвых к дорогим.
    products = Product.objects.order_by('price', 'id')
    if max_price:
        # Адрес можно набрать вручную. Проверяем, что там целое число от 0 до 999999.
        if max_price.isdecimal() and len(max_price) <= 6:
            budget = int(max_price)
            products = products.filter(price__lte=budget)
            max_price = str(budget)
        else:
            error = 'Введите целое число от 0 до 999999.'
            max_price = ''

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'show_budget': True,  # Включаем блок с формой в шаблоне.
        'max_price': max_price,  # Оставляем введённое число в поле после обновления.
        'error': error,
    })


# ПРОВЕРКА: откройте /?max_price=abc. Теперь видны подсказка и все товары.
# Затем введите 100 в поле и убедитесь, что ограничение цены снова работает.
