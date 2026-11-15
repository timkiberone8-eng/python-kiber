from django.shortcuts import render

from .models import Product


def home(request):
    products = Product.objects.filter(price__lte=100).order_by('price', 'id')
    return render(request, 'catalog/product_list.html', {'products': products})
