from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm, PasswordResetForm
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.account_activate, name='account_activate'),
    path('registartion-success', views.registration_success, name="registration_success"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_page.html'), name="password_reset_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_resetting_form.html',
                                                                 form_class=PasswordResetForm,
                                                                 email_template_name='registration/password_resetting_email.html',
                                                                 success_url='/password-reset-done/'),
         name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirmation.html",
                                                     success_url='/password-reset-complete/'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_page.html'), name="password_reset_complete"),
    path('', views.home, name='home'),
]
