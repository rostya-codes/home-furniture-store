from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  # main app
    path('catalog/', include('goods.urls', namespace='catalog')),  # goods app
]

# 2:43:28
