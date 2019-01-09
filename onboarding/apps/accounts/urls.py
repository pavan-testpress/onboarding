from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form = UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('', views.home, name='home'),
]
