from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist

from .models import User


class UserLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
            valid = user.check_password(password)
            if not valid:
                self.add_error('password', 'Invalid password.')
        except ObjectDoesNotExist:
            self.add_error('username', 'User does not exist')
        return super().clean()
