from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Folder
from .filters import FolderFilter


@method_decorator(login_required, name='dispatch')
class FolderListView(ListView):
    template_name = 'bookmarks/folder_list.html'
    model = Folder
    context_object_name = 'folders'
    paginate_by = 10

    def get_queryset(self):
        filtered_data = FolderFilter(request=self.request, data=self.request.GET, queryset=super().get_queryset())
        return filtered_data.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(FolderListView, self).get_context_data()
        data['sort'] = 'name'
        if 'sort' in self.request.GET:
            data['sort'] = self.request.GET['sort']
            if data['sort'] not in ['-modified', '-created', 'name']:
                data['sort'] = 'name'
        if 'name' in self.request.GET:
            data['name'] = self.request.GET['name']
        return data
