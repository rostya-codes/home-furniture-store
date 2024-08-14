from lib2to3.fixes.fix_input import context
from unicodedata import category

from django.shortcuts import render, get_object_or_404

from goods.models import Product


def catalog(request, category_slug):

    if category_slug == 'all':
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category__slug=category_slug)

    context = {
        'title': 'Home - Каталог',
        'goods': goods
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug=None, product_id=None):

    if product_id:
        product = Product.objects.get(id=product_id)
    else:
        product = Product.objects.get(slug=product_slug)

    context = {
        'product': product
    }

    return render(request, 'goods/product.html', context)
