from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


def home(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/home.html')
    else:
        return HttpResponseRedirect(reverse('accounts:login'))
