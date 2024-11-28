from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.views.generic import FormView
from rest_framework.reverse import reverse_lazy

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():  # Атомарная(цельная) транзакция
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Create order
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get']
                    )
                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                  В наличии - {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity
                        )
                        product.quantity -= quantity
                        product.save()

                    # Очистить корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect('user:profile')
        except ValidationError as e:
            messages.warning(self.request, str(e))
            return redirect('cart:order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context
