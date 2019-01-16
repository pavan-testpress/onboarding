from django.forms import ModelForm, forms

from .models import Folder, Bookmark


class FolderCreateForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            Folder.objects.get(created_by=self.user, name__iexact=name)
        except Folder.DoesNotExist:
            return name
        raise forms.ValidationError('Folder already exists.')

    def save(self, commit=True):
        folder = super().save(commit=False)
        folder.created_by = self.user
        folder.save()
        return folder


class BookmarkCreateForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['name','url']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('place_user')
        super().__init__(*args, **kwargs)

    def clean(self):
        name = self.cleaned_data['name']
        url = self.cleaned_data['url']
        try:
            Bookmark.objects.get(created_by=self.user, name__iexact=name)
            self.add_error('name', 'Bookmark name already exists.')
        except Bookmark.DoesNotExist:
            try:
                Bookmark.objects.get(created_by=self.user, url__iexact=url)
                self.add_error('url', 'Url already exists.')
            except Bookmark.DoesNotExist:
                return super().clean()

    def save(self, commit=True):
        bookmark = super().save(commit=False)
        bookmark.created_by = self.user
        bookmark.save()
        return bookmark