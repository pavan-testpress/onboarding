from django.test import TestCase

from exam import Exam, before

from apps.bookmarks.models import Folder, Bookmark
from apps.accounts.models import User


class ModelTestCases(Exam, TestCase):
    @before
    def insert_sample_data_into_folders_and_bookmarks(self):
        self.user = User.objects.create_user(first_name='pavan kumar', last_name='kuppala', username='pavankumar',
                                             email='pavancse17@gmail.com', is_active=True)
        self.user.set_password('143Pavan..')
        self.user.save()
        Folder.objects.create(name='Bbc sdf', created_by=self.user)
        Folder.objects.create(name='Dbc', created_by=self.user)
        Folder.objects.create(name='Abc', created_by=self.user)
        Bookmark.objects.create(name='zasd dfs', created_by=self.user, url='https://www.google.com')
        Bookmark.objects.create(name='assd', created_by=self.user, url='https://www.google.com')
        Bookmark.objects.create(name='casd', created_by=self.user, url='https://www.google.com')

    def test_folder_ordering(self):
        self.assertQuerysetEqual(Folder.objects.all(), Folder.objects.all().order_by('name'), lambda x: x)

    def test_folder_slug(self):
        self.assertEqual(Folder.objects.get(name='Bbc sdf').slug, 'bbc-sdf')

    def test_bookmark_ordering(self):
        self.assertQuerysetEqual(Bookmark.objects.all(), Bookmark.objects.all().order_by('name'), lambda x: x)

    def test_bookmark_slug(self):
        self.assertEqual(Bookmark.objects.get(name='zasd dfs').slug, 'zasd-dfs')
