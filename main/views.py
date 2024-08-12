from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Category


def index(request) -> HttpResponse:

    categories = Category.objects.all()

    context: dict[str, str] = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
        'categories': categories
    }

    return render(request, 'main/index.html', context)


def about(request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том почему этот магазин такой классный, и такой хороший товар.'
    }

    return render(request, 'main/about.html', context)
