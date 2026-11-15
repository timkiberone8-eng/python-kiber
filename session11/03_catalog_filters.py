# ШАГ 3. Читаем бюджет из адреса и фильтруем каталог
# ОТКРЫТЬ: catalog/views.py — приложение рядом с manage.py.
# ДЕЙСТВИЕ: замените только home. Возьмите шаблон из материалов занятия 11.
#
# Найдите поле «Бюджет до, ₽» в catalog/templates/catalog/product_list.html.
# У поля есть name="max_price". При отправке формы с method="get" именно
# это имя попадёт в адрес вместе с суммой, например /?max_price=60.

from django.shortcuts import render

from .models import Product


def home(request):
    max_price = request.GET.get('max_price', '')
    products = Product.objects.order_by('price', 'id')

    # request.GET вернул строку "60". Для запроса к базе превращаем её в число.
    # Пустая строка пропускает if, поэтому в этом случае видны все товары.
    if max_price:
        budget = int(max_price)
        products = products.filter(price__lte=budget)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'show_budget': True,  # Показать форму над карточками.
        'max_price': max_price,  # Вернуть введённую строку в поле.
    })


# ПРОВЕРКА: сначала откройте /?max_price=60 вручную. Затем введите 60 в поле.
# В обоих случаях выборка будет одинаковой. «Сбросить» возвращает адрес /.
# В этом учебном примере используйте числа или пустое поле. Что делать со
# значением /?max_price=abc, разберём следующим шагом.
