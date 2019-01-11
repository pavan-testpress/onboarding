from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as my_login
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from .forms import UserCreationForm
from .models import User
from .tokens import account_activation_token


@login_required
def home(request):
    return render(request, 'accounts/home.html')


def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        my_login(request, user)
        return HttpResponse('<span>Thank you for your email confirmation. Now you can <a href="/login/">login</a> your account.</span>')
    return HttpResponse('Activation link is invalid!')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:home'))
    form = UserCreationForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        message = render_to_string('registration/account_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your account.'
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'pavan1995143.pavan@gmail.com', [to_email, ])
        return HttpResponseRedirect(reverse('accounts:registration_success'))
    return render(request, 'registration/signup.html', {'form': form})

def registration_success(request):
    return HttpResponse('Please confirm your email address to complete the registration')