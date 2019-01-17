from django.urls import path

from . import views

app_name = "bookmarks"

urlpatterns = [
    path('', views.FolderListView.as_view(), name="folders"),
]
