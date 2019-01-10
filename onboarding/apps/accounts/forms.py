from django.contrib.auth.forms import AuthenticationForm

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
        except User.DoesNotExist:
            self.add_error('username', 'User does not exist')
        return super().clean()
