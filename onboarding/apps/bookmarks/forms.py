from django.forms import ModelForm, forms

from .models import Folder


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
