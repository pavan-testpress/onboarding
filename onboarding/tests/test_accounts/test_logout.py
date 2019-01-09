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
        }
        User.objects.create_user(first_name=user['first_name'], last_name=user['last_name'],
                                 username=user['username'], email=user['email'],
                                 is_active=True, password='143Pavan..')

    def test_logout(self):
        self.client.login(username="pavankumar", password="143Pavan..")
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertRedirects(response, '/login/?next=/')
