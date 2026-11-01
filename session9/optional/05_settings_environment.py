import os
import re

schema = os.environ['PGSCHEMA']
if not re.fullmatch(r'catalog_[a-z0-9_]+', schema):
    raise ValueError('PGSCHEMA: catalog_ и далее маленькие латинские буквы, цифры, _')

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ['PGDATABASE'],
    'USER': os.environ['PGUSER'],
    'PASSWORD': os.environ['PGPASSWORD'],
    'HOST': os.environ.get('PGHOST', '127.0.0.1'),
    'PORT': os.environ.get('PGPORT', '5432'),
    'OPTIONS': {'options': '-c search_path=' + schema},
}}
