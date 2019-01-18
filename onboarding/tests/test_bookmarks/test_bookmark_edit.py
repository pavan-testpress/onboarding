from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import before

from apps.accounts.models import User
from apps.bookmarks.models import Folder, Bookmark


class UpdateBookmarkTestCase(Exam, TestCase):
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
        self.t = Folder.objects.create(name='Testpress', created_by=self.user)
        self.g = Folder.objects.create(name='Google', created_by=self.user)
        Bookmark.objects.create(name='Testpress', url='https://www.testpress.in', folder=self.t, created_by=self.user)
        Bookmark.objects.create(name='Google', url='https://www.google.com', folder=self.g, created_by=self.user)
        self.client.login(username='pavankumar', password='143Pavan..')

    def test_redirect_if_not_logged_in(self):
        """
        Test bookmark update page without logged in the user.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/testpress/1/edit/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark-folders/testpress/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_update_form.html')

    def test_update_view_with_existing_bookmark_name(self):
        response = self.client.post(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}),
                                    {'name': 'Google', 'url': 'https://www.testpress.in'})
        self.assertEqual(response.context['form'].errors['name'], ['Folder already exists.'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_update_form.html')

    def test_update_view_with_existing_bookmark_url(self):
        response = self.client.post(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}),
                                    {'name': 'Testpress', 'url': 'https://www.google.com'})
        self.assertEqual(response.context['form'].errors['url'], ['Url already exists.'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_update_form.html')

    def test_update_view_with_new_bookmark_name(self):
        response = self.client.post(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}),
                                    {'name': 'Testpressnew', 'url': 'https://www.testpress.in', 'folder': 1})
        self.assertRedirects(response, reverse('bookmarks:bookmarks', kwargs={'slug': 'testpress'}))
        assert Bookmark.objects.filter(name='Testpressnew').exists()
        self.assertEqual(Bookmark.objects.filter(name='Testpressnew').count(), 1)

    def test_update_view_with_new_bookmark_url(self):
        response = self.client.post(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}),
                                    {'name': 'Testpress', 'url': 'https://www.testpressnew.in', 'folder': 1})
        self.assertRedirects(response, reverse('bookmarks:bookmarks', kwargs={'slug': 'testpress'}))
        assert Bookmark.objects.filter(url='https://www.testpressnew.in').exists()
        self.assertEqual(Bookmark.objects.filter(url='https://www.testpressnew.in', created_by=self.user).count(), 1)

    def test_update_view_when_moving_to_other_folder(self):
        response = self.client.post(reverse('bookmarks:bookmark_update', kwargs={'slug': 'testpress', 'pk': '1'}),
                                    {'name': 'Testpress', 'url': 'https://www.testpress.in', 'folder': 2})
        self.assertRedirects(response, reverse('bookmarks:bookmarks', kwargs={'slug': 'testpress'}))
        assert Bookmark.objects.filter(url='https://www.testpress.in', folder=self.g).exists()
        self.assertEqual(Bookmark.objects.filter(url='https://www.testpress.in', folder=self.g, created_by=self.user).count(), 1)
