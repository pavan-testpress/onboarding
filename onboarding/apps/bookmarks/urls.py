from django.urls import path

from . import views

app_name = "bookmarks"

urlpatterns = [
    path('', views.FolderListView.as_view(), name="folders"),
    path('create/', views.FolderCreateView.as_view(), name="folder_create"),
    path('<slug>/edit/', views.FolderUpdateView.as_view(), name="folder_update"),
    path('<slug>/delete/', views.FolderDeleteView.as_view(), name="folder_delete"),
    path('<slug>/', views.BookmarkListView.as_view(), name="bookmarks"),
    path('<slug>/create/', views.BookmarkCreateView.as_view(), name="bookmark_create"),
    path('<slug>/<pk>/edit/', views.BookmarkUpdateView.as_view(), name="bookmark_update"),
]
