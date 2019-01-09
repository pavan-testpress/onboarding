from django.test import TestCase
from django.shortcuts import reverse

from apps.accounts.models import User


class AccountsTestCase(TestCase):

    def setUp(self):
        user = {
            'first_name': 'Pavan Kumar',
            'last_name': 'Kuppala',
            'username': 'pavankumar',
            'email': 'pavancse17@gmail.com',
            'password1': '143Pavan..',
            'password2': '143Pavan..',

        }
        User.objects.create_user(first_name=user['first_name'], last_name=user['last_name'],
                                 username=user['username'], email=user['email'],
                                 is_active=True, password='143Pavan..')

    def test_get_login_page(self):
        """
        Test to get login page.
        """
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, '<input type="text" name="username" autofocus class="textinput textInput form-control" required id="id_username">')
        self.assertContains(response, '<button class="btn btn-success" type="submit">Login</button>')
        self.assertContains(response, '<input type="password" name="password" class="textinput textInput form-control" required id="id_password">')

    def test_try_to_login_with_invalid_credentials(self):
        """
        Test to login with invalid credentials
        """
        response = self.client.post(reverse('accounts:login'), {'username': 'dsfsdfs', 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'username': ['User does not exist']})
        response = self.client.post(reverse('accounts:login'), {'username': 'pavankumar', 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'password': ['Invalid password.']})
        response = self.client.post(reverse('accounts:login'), {'username': 'pavafsfs', 'password': '143Pavan..'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'username': ['User does not exist']})
        response = self.client.post(reverse('accounts:login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['username'], ['This field is required.', 'User does not exist'])
        self.assertEqual(response.context['form'].errors['password'], ['This field is required.'])

    def test_post_login_page(self):
        """
        Test to login existing user.
        """
        response = self.client.post(reverse('accounts:login'), {'username': 'pavankumar', 'password': '143Pavan..'})
        self.assertRedirects(response, reverse('accounts:home'))
