from django.db import models

from goods.models import Product
from users.models import User


class CartQuerySet(models.QuerySet):
    """ Тут можно добавить дополнительные функции пакетного менеджера """

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')  # Кому принадлежит корзина
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')  # Связанный продукт
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)  # Session key for unauthorized users
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')  # Дата создания корзины

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    objects = CartQuerySet().as_manager()  # Переопределение пакетного менеджера

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
