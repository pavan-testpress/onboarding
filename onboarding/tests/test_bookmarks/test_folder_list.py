from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import before

from apps.accounts.models import User
from apps.bookmarks.models import Folder


class FolderListTestCase(Exam, TestCase):
    user = None

    @before
    def inserting_sample_data_and_login_user(self):
        """
        This function will execute before for each testcase.
        Some sample bookmarks and folders will be saved in database.
        """
        self.user = User.objects.create_user(first_name='pavan kumar', last_name='kuppala', username='pavankumar',
                                             email='pavancse17@gmail.com', is_active=True)
        self.user.set_password('143Pavan..')
        self.user.save()
        for i in range(23):
            Folder.objects.create(name='folder' + str(i), created_by=self.user)
        self.client.login(username='pavankumar', password='143Pavan..')

    def test_redirect_if_not_logged_in(self):
        """
        Test folder list page without logged in the user.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark-folders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['folders']) == 10)

    def test_lists_all_folders(self):
        """
            Test Sorting feature by name in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:folders') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['folders']) == 3)

    def test_get_folder_list_view_by_name(self):
        """
        Test Sorting feature by name in folder list page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=name")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_created_date(self):
        """
        Test sort by created date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-created")
        folders = Folder.objects.filter(created_by=self.user).order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_modified_date(self):
        """
        Test sort by modified date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modified")
        folders = Folder.objects.filter(created_by=self.user).order_by('-modified')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_unknown_sorting_order(self):
        """
        Testing folderlist page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modisadasd")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_for_searched_folder_by_name(self):
        """
        Test searching feature by name in folder list page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=name&name=test")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='test').order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 0)

        response = self.client.get(reverse('bookmarks:folders') + "?sort=name&name=0")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='0').order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 3)

    def test_get_folder_list_for_searched_folder_by_modified_date(self):
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modified&name=0")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='0').order_by('-modified')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 3)

    def test_get_folder_list_for_searched_folder_by_created_date(self):
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-created&name=0")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='0').order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 3)
