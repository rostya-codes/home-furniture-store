from django import template

from goods.models import Category


register = template.Library()


# Шаблонный тег для получения категорий
@register.simple_tag()
def tag_categories():
    return Category.objects.all()
