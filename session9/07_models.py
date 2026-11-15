# ШАГ 7. Описываем товар
# ОТКРЫТЬ: catalog/models.py
# ДЕЙСТВИЕ: заменить содержимое целиком

from django.db import models             # Типы полей и базовый класс модели


class Product(models.Model):             # Один объект — один товар
    name = models.CharField(max_length=100)  # Название, до 100 символов
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Цена, 2 знака

    def __str__(self):                    # Как товар подписан в админке
        return self.name

# Таблица пока НЕ создана: следующий файл — 08_migrations.txt
