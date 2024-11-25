from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'Магазин мебели - Home'
        return context


# def index(request) -> HttpResponse:
#     context: dict[str, str] = {
#         'title': 'Home - Главная',
#         'content': 'Магазин мебели HOME',
#     }
#     return render(request, 'main/index.html', context)


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = 'О нас'
        context['text_on_page'] = 'Текст о том почему этот магазин такой классный, и какой хороший товар.'
        return context


# def about(request) -> HttpResponse:
#     context: dict[str, str] = {
#         'title': 'Home - О нас',
#         'content': 'О нас',
#         'text_on_page': 'Текст о том почему этот магазин такой классный, и такой хороший товар.'
#     }
#     return render(request, 'main/about.html', context)
