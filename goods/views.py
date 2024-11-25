from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.models import Product
from goods.utils import q_search


class CatalogView(ListView):
    model = Product
    # queryset = Product.objects.all().order_by('-id')  # similar to model =
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 3
    allow_empty = False  # Если товаров в какой-то категории не будет, то выведется ошибка 404

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if category_slug == 'all':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)
        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        # self.categories = Category.objects.all()
        return goods


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Каталог'
        context['slug_url'] = self.kwargs.get('category_slug')
        # context['categories'] = Category.objects.all()
        return context


class ProductView(DetailView):
    # model = Product
    # slug_field = 'slug'
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


# def catalog(request, category_slug=None):
#
#     page = request.GET.get('page', 1)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
#     on_sale = request.GET.get('on_sale', None)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
#     order_by = request.GET.get('order_by', None)  # Получить из ссылки номер страницы по ключу, дефолт значение - 1
#     query = request.GET.get('q', None)
#
#     if category_slug == 'all':
#         goods = Product.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Product.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#     if order_by and order_by != 'default':
#         goods = goods.order_by(order_by)
#
#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page))
#
#     context = {
#         'title': 'Home - Каталог',
#         'goods': current_page,
#         'slug_url': category_slug,
#     }
#     return render(request, 'goods/catalog.html', context)


# def product(request, product_slug=None, product_id=None):
#     if product_id:
#         product = Product.objects.get(id=product_id)
#     else:
#         product = Product.objects.get(slug=product_slug)
#     context = {'product': product}
#     return render(request, 'goods/product.html', context)
