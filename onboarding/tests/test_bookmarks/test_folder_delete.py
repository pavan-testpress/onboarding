from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam, before

from apps.accounts.models import User
from apps.bookmarks.models import Folder, Bookmark


class DeleteFolderTestCase(Exam, TestCase):
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
        Test if folder delete page without logged in the user
        redirects to login or not.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/testpress/delete/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark-folders/testpress/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_delete_confirm.html')

    def test_first_delete_folder(self):
        """
        Checking behaviour of first folder.
            - It should create a new Uncategorized folder.
            - It should move all bookmarks present inside that folder to Uncategorized.
        """
        self.assertEqual(Folder.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(pk=1).folder.name, 'Testpress')
        response = self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        assert Folder.objects.filter(name='Uncategorized', created_by=self.user).exists()
        self.assertEqual(Bookmark.objects.get(pk=1).folder.name, 'Uncategorized')
        self.assertRedirects(response, reverse('bookmarks:folders'))
        self.assertEqual(Folder.objects.count(), 2)
        self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'google'}))
        self.assertEqual(Folder.objects.count(), 1)

    def test_delete_when_Uncategorized_folder_exists(self):
        """
        Checking behaviour of when Uncategorized folder exists.
            - It should move bookmarks to Uncategorized folder
        """
        f = Folder.objects.create(name="Uncategorized", created_by=self.user)
        response = self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        self.assertRedirects(response, reverse('bookmarks:folders'))
        self.assertEqual(f.folder.count(), 1)
        response = self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'google'}))
        self.assertEqual(f.folder.count(), 2)

    def test_delete_Uncategorized_folder_itself(self):
        """
        Checking behaviour of when Uncategorized folder deleted.
            - It should delete all bookmarks inside Uncategorized and folder itself.
        """
        f = Folder.objects.create(name="Uncategorized", created_by=self.user)
        response = self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'testpress'}))
        self.assertRedirects(response, reverse('bookmarks:folders'))
        self.assertEqual(f.folder.count(), 1)
        self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'google'}))
        self.assertEqual(f.folder.count(), 2)
        self.client.post(reverse('bookmarks:folder_delete', kwargs={'slug': 'uncategorized'}))
        self.assertEqual(Bookmark.objects.count(), 0)
        self.assertEqual(Folder.objects.count(), 0)
