from django.http import HttpResponse

from .models import Product


def home(request):
    products = Product.objects.all()
    lines = []

    for product in products:
        lines.append(f'{product.name} — {product.price} ₽')

    text = '\n'.join(lines) or 'Товаров пока нет'
    return HttpResponse(text, content_type='text/plain; charset=utf-8')
