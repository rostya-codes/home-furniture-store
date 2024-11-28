from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                # Delete
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # Add new authorized user carts from anonymous session
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f'{user.username}, Вы вошли в игру!')
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f'{user.username}, Вы успешно зарегистрированы и вошли в аккаунт')
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'
        context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related('product')
            )
        ).order_by('-id')
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page:
            return redirect_page
        return reverse_lazy('main:index')


# @login_required
# def logout(request):
#     messages.success(request, f'{request.user.username}, Вы вышли из аккаунта')  # Success message
#     auth.logout(request)
#     return redirect(reverse('main:index'))
