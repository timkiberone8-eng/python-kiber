from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# 

# Create your views here.
def home(request):
    max_price = request.GET.get('max_price', '')
    products = Product.objects.order_by('price', 'id')

    if max_price:
        budget = int(max_price)
        products = products.filter(price__lte=budget)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'show_budget': True,
        'max_price': max_price,
    })