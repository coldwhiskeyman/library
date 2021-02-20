from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserLoginView(LoginView):
    """
    Представление страницы авторизации пользователя
    """
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('api-root')


class UserLogoutView(LogoutView):
    """
    Представление выхода из системы
    """
    next_page = reverse_lazy('api-root')


class UserCreateView(CreateView):
    """
    Представление страницы регистрации пользователя
    """
    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('api-root')
