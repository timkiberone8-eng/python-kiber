from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.

def home(request):
    # return HttpResponse('<h1>Каталог работает</h1>')
    products = Product.objects.all()
    lines = []

    for product in products:
        lines.append(f'{product.name} - {product.price}')

    text = '\n'.join(lines) or 'Товаров нет'

    return HttpResponse(text, content_type='text/plain, charset=utf-8')