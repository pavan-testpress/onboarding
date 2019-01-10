from django.test import TestCase
from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.accounts.models import User


class ForgotPasswordTestCases(TestCase):
    def setUp(self):
        user = {
            'first_name': 'Pavan Kumar',
            'last_name': 'Kuppala',
            'username': 'pavankumar',
            'email': 'pavancse17@gmail.com',
        }
        User.objects.create_user(first_name=user['first_name'], last_name=user['last_name'], username=user['last_name'], email=user['email'], password="'143Pavan..'", is_active=True)

    def test_to_get_forgot_password(self):
        response = self.client.get(reverse("accounts:password_reset"))
        self.assertTemplateUsed(response, 'registration/password_resetting_form.html')

    def test_post_email_forgot_password(self):
        response = self.client.post(reverse("accounts:password_reset"), {'email': 'pavancse17@gmail.com'})
        self.assertEqual(response.context['domain'], 'testserver')
        self.assertEqual(response.context['uid'],
                         urlsafe_base64_encode(force_bytes(response.context['user'].pk)).decode())

    def test_reseting_password(self):
        response = self.client.post(reverse("accounts:password_reset"), {'email': 'pavancse17@gmail.com'})
        forgot_page = self.client.get(reverse('accounts:password_reset_confirm', kwargs={'uidb64': response.context['uid'], 'token': response.context['token']}), follow=True)
        forgot = self.client.post(forgot_page.redirect_chain[0][0], {'new_password1': 'Pavan143..', 'new_password2': 'Pavan143..'})
        self.assertRedirects(forgot, reverse('accounts:password_reset_complete'))
