from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# 

# Create your views here.
def home(request):
    products = Product.objects.filter(price__lte=100).order_by('price', 'id')
    lines = []

    for product in products:
        lines.append(f'{product.name} - {product.price}')

    text = '\n'.join(lines) or 'Товаров пока нет'

    return render(request, 'catalog/product_list.html', {'products': products})