from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Folder, Bookmark
from .filters import FolderFilter, BookmarkFilter
from .forms import FolderCreateForm, BookmarkCreateForm, FolderUpdateForm, BookmarkUpdateForm


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
        self.filtered_data = BookmarkFilter(request=self.request, data=self.request.GET, queryset=super().get_queryset())
        return self.filtered_data.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(BookmarkListView, self).get_context_data()
        data['selected_folder'] = self.kwargs['slug']
        data['folders'] = Folder.objects.filter(created_by=self.request.user).order_by('name')
        data['filter_form'] = self.filtered_data.form
        return data


@method_decorator(login_required, name='dispatch')
class FolderCreateView(CreateView):
    form_class = FolderCreateForm
    template_name = 'bookmarks/folder_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@method_decorator(login_required, name='dispatch')
class BookmarkCreateView(CreateView):
    form_class = BookmarkCreateForm
    template_name = 'bookmarks/bookmark_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'folder': self.kwargs['slug']})
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['selected_folder'] = self.kwargs['slug']
        return data

    def get_success_url(self):
        url = reverse('bookmarks:bookmarks', kwargs={'slug': self.kwargs['slug']})
        return url


@method_decorator(login_required, name='dispatch')
class FolderUpdateView(UpdateView):
    model = Folder
    form_class = FolderUpdateForm
    template_name = 'bookmarks/folder_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        return Folder.objects.filter(created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class BookmarkUpdateView(UpdateView):
    model = Bookmark
    form_class = BookmarkUpdateForm
    template_name = 'bookmarks/bookmark_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user, 'pk': self.kwargs['pk']})
        return kwargs

    def get_queryset(self):
        return Bookmark.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['form'].fields["folder"].queryset = Folder.objects.filter(created_by=self.request.user)
        data['selected_folder'] = self.kwargs['slug']
        return data

    def get_success_url(self):
        url = reverse('bookmarks:bookmarks', kwargs={'slug': self.kwargs['slug']})
        return url
