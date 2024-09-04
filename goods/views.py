from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator

from goods.models import Product
from goods.utils import q_search


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
    on_sale = request.GET.get('on_sale', None)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
    order_by = request.GET.get('order_by', None)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug,
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
