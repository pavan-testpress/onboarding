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
        name = self.cleaned_data['name'].capitalize()
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
        fields = ['name', 'url']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.folder = kwargs.pop('folder')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        return self.cleaned_data['name'].capitalize()

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
        if self.folder == 'all':
            try:
                folder = Folder.objects.get(name='Uncategorized', created_by=self.user)
            except Folder.DoesNotExist:
                folder = Folder.objects.create(name="Uncategorized", created_by=self.user)
        else:
            folder = Folder.objects.get(slug=self.folder, created_by=self.user)
        bookmark.folder = folder
        bookmark.save()
        return bookmark


class FolderUpdateForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name'].capitalize()
        count = Folder.objects.filter(created_by=self.user, name__iexact=name).count()
        if count == 0:
            return name
        raise forms.ValidationError('Folder already exists.')


class BookmarkUpdateForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['name', 'url', 'folder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.pk = kwargs.pop('pk')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name'].capitalize()
        bookmark_pks = list(Bookmark.objects.filter(created_by=self.user, name__iexact=name).values_list('id', flat=True))
        if int(self.pk) in bookmark_pks or len(bookmark_pks) == 0:
            return name
        raise forms.ValidationError('Folder already exists.')

    def clean_url(self):
        url = self.cleaned_data['url']
        bookmark_pks = list(Bookmark.objects.filter(created_by=self.user, url=url).values_list('id', flat=True))
        if int(self.pk) in bookmark_pks or len(bookmark_pks) == 0:
            return url
        raise forms.ValidationError('Url already exists.')
