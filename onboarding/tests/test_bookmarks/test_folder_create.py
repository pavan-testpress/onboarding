from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import before

from apps.accounts.models import User
from apps.bookmarks.models import Folder


class FolderCreateTestCase(Exam, TestCase):
    user = None

    @before
    def inserting_sample_data_and_login_user(self):
        """
        This function will execute before for each testcase.
        Some sample folder will be saved in database.
        """
        self.user = User.objects.create_user(first_name='pavan kumar', last_name='kuppala', username='pavankumar',
                                             email='pavancse17@gmail.com', is_active=True)
        self.user.set_password('143Pavan..')
        self.user.save()
        Folder.objects.create(name='Testpress', created_by=self.user)
        self.client.login(username='pavankumar', password='143Pavan..')

    def test_redirect_if_not_logged_in(self):
        """
        Test folder create page without logged in the user.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:folder_create'))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/create/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark-folders/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folder_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folder_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_create_form.html')

    def test_create_view_with_existing_folder(self):
        response = self.client.post(reverse('bookmarks:folder_create'), {'name': 'Testpress'})
        self.assertEqual(response.context['form'].errors['name'], ['Folder already exists.'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_create_form.html')

    def test_create_view_with_new_folder(self):
        response = self.client.post(reverse('bookmarks:folder_create'), {'name': 'Google'})
        self.assertRedirects(response, reverse('bookmarks:folders'))
        assert Folder.objects.filter(name='Google').exists()
