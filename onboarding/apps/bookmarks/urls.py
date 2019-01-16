from django.urls import path

from . import views

app_name = "bookmarks"

urlpatterns = [
    path('', views.FolderListView.as_view(), name="folders"),
    path('create/', views.FolderCreateView.as_view(), name="folder_create"),
    path('<slug>/', views.BookmarkListView.as_view(), name="bookmarks"),
    path('<slug>/create/', views.BookmarkCreateView.as_view(), name="bookmark_create"),
]
