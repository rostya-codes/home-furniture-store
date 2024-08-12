from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  # main app
    path('catalog/', include('goods.urls', namespace='catalog')),  # goods app
] + debug_toolbar_urls()

# 2:43:28
