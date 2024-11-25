from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    # path('<slug:category_slug>/<int:page>/', views.catalog, name='index'),
    path('product/<int:product_id>/', views.ProductView.as_view(), name='product'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
