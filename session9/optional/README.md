# Необязательные продолжения

Начинай только после сохранённого товара в админке. Основной проход находится уровнем выше: [README](../README.md).

## ORM: чтение без готового ответа самостоятельной задачи

Из папки с manage.py: `python manage.py shell`, затем:

```python
from catalog.models import Product
print(list(Product.objects.values_list('name', 'price')))
exit()
```

Самостоятельно попробуй выбрать товары не дороже 100 и отсортировать по цене.

## Список на странице

В catalog/views.py добавь импорты и функцию из [09_product_list_view.py](09_product_list_view.py), сохрани home. Во внутреннем mysite/urls.py в urlpatterns добавь `path('catalog/', views.product_list, name='product-list'),`. Создай catalog/templates/catalog/product_list.html и вставь [10_product_list.html](10_product_list.html). Открой /catalog/, добавь товар через /admin/ и обнови список.

## Позднее: отдельные маршруты

[02_catalog_urls.py](02_catalog_urls.py) — прежний образец с home/about/contacts. Не вставляй его поверх основного прохода без добавления отсутствующих about/contacts в views.py. Для разделения маршрутов создай catalog/urls.py и подключи его через include в главном urls.py. Сегодня это не требуется.

## Позднее: схемы и переменные окружения

Эти файлы сохранены из расширенного варианта и не запускаются автоматически: [04_check_db.py](04_check_db.py), [05_settings_environment.py](05_settings_environment.py), [06_check_django.py](06_check_django.py).

Это отдельное упражнение, не замена одного файла: сначала выбрать учебную базу, создать свою новую схему через check_db.py, задать в терминале PGDATABASE/PGUSER/PGPASSWORD/PGHOST/PGPORT/PGSCHEMA, затем заменить настройки расширенным образцом. Смена схемы означает другой набор таблиц: перед миграциями проверить подключение. Перенос данных основной базы этим не выполняется.
