from django.contrib.admin import site

from apps.bookmarks.models import Folder, Bookmark

site.register([Folder, Bookmark])
