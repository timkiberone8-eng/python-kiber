# ШАГ 9. Показываем товары в админке
# ОТКРЫТЬ: catalog/admin.py
# ДЕЙСТВИЕ: заменить содержимое целиком

from django.contrib import admin         # Готовый интерфейс управления
from .models import Product              # Наша модель товара

admin.site.register(Product)             # Добавить Product в интерфейс админки

# Эта строка НЕ создаёт таблицу: таблицу уже создала миграция
# Далее — команды из 10_admin_commands.txt
