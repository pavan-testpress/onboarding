from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
            if (user.is_active is False) and (valid is True):
                self.add_error('username', 'Please verify your email to login.')
        except User.DoesNotExist:
            self.add_error('username', 'User does not exist')
        return super(UserLoginForm, self).clean()


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'User already exists.')
        elif User.objects.filter(email=email).exists():
            self.add_error('email', 'User with given email already exists.')
        return super(UserCreationForm, self).clean()
