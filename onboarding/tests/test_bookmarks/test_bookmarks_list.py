from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import before

from apps.accounts.models import User
from apps.bookmarks.models import Folder, Bookmark


class BookmarkListTestCase(Exam, TestCase):
    user = None
    f = None

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
        f = Folder.objects.create(name='folder1', created_by=self.user)
        g = Folder.objects.create(name='folder2', created_by=self.user)
        for i in range(7):
            Bookmark.objects.create(name='bookmark' + str(i), url="https://www.test_url_" + str(i) + ".com", folder=f, created_by=self.user)
        for i in range(12):
            Bookmark.objects.create(name='bookmark' + str(i), url="https://www.test_url_" + str(i) + ".com", folder=g, created_by=self.user)
        self.client.login(username='pavankumar', password='143Pavan..')

    def test_redirect_if_not_logged_in(self):
        """
        Test bookmarks list page without logged in the user.
        """
        self.client.logout()
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}))
        self.assertRedirects(response, '/login/?next=/bookmark-folders/folder1/')

    def test_view_url_exists_at_desired_location(self):
<<<<<<< HEAD
        response = self.client.get('/bookmark-folders/folder1/')
=======
        response = self.client.get('/bookmark-folders/folder-1/')
>>>>>>> 55ce71a... Add BookmarksList
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['bookmarks']) == 5)

    def test_lists_all_bookmarks(self):
        """
            Test Sorting feature by name in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['bookmarks']) == 2)

    def test_get_bookmarks_list_view_by_name(self):
        """
        Test Sorting feature by name in bookmarks list page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=name")
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=1).order_by('name')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmarks_list_view_by_created_date(self):
        """
        Test sort by created date in bookmarks list page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=-created")
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=1).order_by('-created')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmarks_list_view_by_modified_date(self):
        """
        Test sort by modified date in bookmarks list page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=-modified")
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=1).order_by('-modified')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmarks_list_unknown_sorting_order(self):
        """
        Testing bookmarks list page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=-modgfdgdfified")
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=1).order_by('name')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmarks_list_for_searched_bookmarks_by_name(self):
        """
        Test searching feature by name in bookmarks list page.
        """
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=name&name=test")
        bookmarks = Bookmark.objects.filter(created_by=self.user, name__icontains='test', folder=1).order_by('name')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 0)

        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=name&name=0")
        bookmarks = Bookmark.objects.filter(created_by=self.user, name__icontains='0', folder=1).order_by('name')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 1)

    def test_get_bookmarks_list_for_searched_bookmark_by_modified_date(self):
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=-modified&name=book")
        bookmarks = Bookmark.objects.filter(created_by=self.user, name__icontains='book', folder=1).order_by('-modified')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 5)

    def test_get_bookmarks_list_for_searched_bookmark_by_created_date(self):
        response = self.client.get(reverse('bookmarks:bookmarks', kwargs={'slug': 'folder1'}) + "?sort=-created&name=book")
        bookmarks = Bookmark.objects.filter(created_by=self.user, name__icontains='book', folder=1).order_by('-created')[:5]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 5)
