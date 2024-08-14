from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    # Фрагмент url адресов
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'  # Альтернативное название для отображения в админ панели
        verbose_name_plural = 'Категории'  # Множественное число


class Product(models.Model):

    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    # Фрагмент url адресов
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name} | Количество - {self.quantity}'

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'  # Альтернативное название для отображения в админ панели
        verbose_name_plural = 'Продукты'  # Множественное число

    def display_id(self):
        return f'{self.id:05}'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
