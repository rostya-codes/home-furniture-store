from django import template

from carts.models import Cart

register = template.Library()


# Шаблонный тег для получения категорий
@register.simple_tag()
def user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)  # Все корзины конкретного пользователя
