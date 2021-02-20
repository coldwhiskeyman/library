from django.urls import path

from users.views import UserCreateView, UserLoginView, UserLogoutView


urlpatterns = [
    path('register', UserCreateView.as_view(), name='user_create'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
]
