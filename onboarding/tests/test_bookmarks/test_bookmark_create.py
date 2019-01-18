from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import before

from apps.accounts.models import User
from apps.bookmarks.models import Folder, Bookmark


class BookmarkCreateTestCase(Exam, TestCase):
    user = None

    @before
    def inserting_sample_data_and_login_user(self):
        """
        This function will execute before for each testcase.
        Some sample folder and bookmark will be saved in database.
        """
        self.user = User.objects.create_user(first_name='pavan kumar', last_name='kuppala', username='pavankumar',
                                             email='pavancse17@gmail.com', is_active=True)
        self.user.set_password('143Pavan..')
        self.user.save()
        f = Folder.objects.create(name='Testpress', created_by=self.user)
        Bookmark.objects.create(name='Testpress', url='https://www.testpress.in', created_by=self.user, folder=f)
        self.client.login(username='pavankumar', password='143Pavan..')

    def test_redirect_if_not_logged_in(self):
        """
        Test bookmark create page without logged in the user.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/testpress/create/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark-folders/testpress/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_create_form.html')

    def test_create_view_with_existing_bookmark_name(self):
        response = self.client.post(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}), {'name': 'Testpress', 'url': 'https://www.testpress.in'})
        self.assertEqual(response.context['form'].errors['name'], ['Bookmark name already exists.'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_create_form.html')

    def test_create_view_with_existing_bookmark_url(self):
        response = self.client.post(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}), {'name': 'Test', 'url': 'https://www.testpress.in'})
        self.assertEqual(response.context['form'].errors['url'], ['Url already exists.'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_create_form.html')

    def test_create_view_with_new_bookmark_inside_folder(self):
        response = self.client.post(reverse('bookmarks:bookmark_create', kwargs={'slug': 'testpress'}),
                                    {'name': 'Test', 'url': 'https://www.test.in'})
        self.assertRedirects(response, reverse('bookmarks:bookmarks', kwargs={'slug': 'testpress'}))
        assert Bookmark.objects.filter(name='Test').exists()
        self.assertEqual(Folder.objects.get(name='Testpress').folder.count(), 2)

    def test_create_view_with_new_bookmark_from_all_bookamarks(self):
        response = self.client.post(reverse('bookmarks:bookmark_create', kwargs={'slug': 'all'}),
                                    {'name': 'Test', 'url': 'https://www.test.in'})
        self.assertRedirects(response, reverse('bookmarks:bookmarks', kwargs={'slug': 'all'}))
        assert Bookmark.objects.filter(name='Test').exists()
        self.assertEqual(Folder.objects.get(name='Uncategorized').folder.count(), 1)
