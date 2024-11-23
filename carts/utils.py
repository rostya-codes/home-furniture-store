from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product')  # Все корзины конкретного пользователя

    if not request.session.session_key:
        request.session.create()  # Присвоить пользователю session_key
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
