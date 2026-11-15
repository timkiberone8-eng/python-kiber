# Занятие 9: каталог товаров на Django

Образцы кода для проекта `mysite`. Пути в шапках файлов указаны относительно папки с `manage.py`; команды выполняются из этой папки. Образцы перепечатывают или копируют в указанные файлы своего проекта, а не запускают отдельно.

```text
mysite/                          ← папка с manage.py
├── manage.py
├── mysite/
│   ├── settings.py
│   └── urls.py
└── catalog/
    ├── views.py
    ├── models.py
    └── admin.py
```

| Шаг | Образец | Где применить |
|---|---|---|
| 2 | [02_create_app.txt](02_create_app.txt) | создать catalog, добавить в INSTALLED_APPS |
| 3 | [03_catalog_views.py](03_catalog_views.py) | catalog/views.py |
| 4 | [04_project_urls.py](04_project_urls.py) | mysite/urls.py; сохранить прежние страницы |
| 5 | [05_create_database.sql](05_create_database.sql) | SQL Shell (psql) |
| 6 | [06_settings_databases.py](06_settings_databases.py) | заменить только DATABASES в mysite/settings.py |
| 7 | [07_models.py](07_models.py) | catalog/models.py |
| 8 | [08_migrations.txt](08_migrations.txt) | терминал рядом с manage.py |
| 9 | [09_admin.py](09_admin.py) | catalog/admin.py |
| 10 | [10_admin_commands.txt](10_admin_commands.txt) | терминал и /admin/ |

Если приложение catalog уже существует, повторно startapp не выполняют. При изменении urls.py сохраняют остальные маршруты и функции. Внутренние папки проекта могут находиться в разных родительских каталогах; важен путь относительно manage.py.

Результат: товар добавляется через админку и остаётся после перезапуска сервера. Настоящий пароль указывают только локально; перед публикацией settings.py секреты нужно убрать. При создании базы не удаляйте уже существующую базу с таким именем.

Дополнительные упражнения: [optional/README.md](optional/README.md).
