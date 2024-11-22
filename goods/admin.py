from django.contrib import admin

from goods.models import Category, Product

# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Поля, которые заполняются автоматически


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Поля, которые заполняются автоматически
    list_display = ('name', 'quantity', 'price', 'discount')
    list_editable = ('quantity', 'price', 'discount')
    search_fields = ('name', 'description')
    list_filter = ('discount', 'quantity', 'category')
    fields = (
        'name',
        'category',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'quantity'
    )
