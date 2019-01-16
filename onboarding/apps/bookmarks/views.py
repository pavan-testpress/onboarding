from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Folder, Bookmark
from .filters import FolderFilter, BookmarkFilter


@method_decorator(login_required, name='dispatch')
class FolderListView(ListView):
    template_name = 'bookmarks/folder_list.html'
    model = Folder
    context_object_name = 'folders'
    paginate_by = 10

    def get_queryset(self):
        self.filtered_data = FolderFilter(request=self.request, data=self.request.GET, queryset=super().get_queryset())
        return self.filtered_data.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(FolderListView, self).get_context_data()
        data['filter_form'] = self.filtered_data.form
        return data


@method_decorator(login_required, name='dispatch')
class BookmarkListView(ListView):
    model = Bookmark
    template_name = 'bookmarks/bookmark_list.html'
    context_object_name = 'bookmarks'
    paginate_by = 5

    def get_queryset(self):
        filtered_data = BookmarkFilter(request=self.request, data=self.request.GET, queryset=super().get_queryset())
        return filtered_data.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(BookmarkListView, self).get_context_data()
        data['selected_folder'] = self.kwargs['slug']
        data['folders'] = Folder.objects.filter(created_by=self.request.user).order_by('name')
        data['sort'] = 'name'
        if 'sort' in self.request.GET:
            data['sort'] = self.request.GET['sort']
            if data['sort'] not in ['-modified', '-created', 'name']:
                data['sort'] = 'name'
        if 'name' in self.request.GET:
            data['name'] = self.request.GET['name']
        return data
