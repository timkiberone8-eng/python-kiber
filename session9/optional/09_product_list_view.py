from django.shortcuts import render
from .models import Product


def product_list(request):
    products = Product.objects.order_by('price', 'id')
    return render(request, 'catalog/product_list.html', {'products': products})
