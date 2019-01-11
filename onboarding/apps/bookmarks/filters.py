import django_filters

from .models import Folder


class FolderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Folder
        fields = ['name']

    def filter_queryset(self, queryset):
        sort = 'name'
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-created', '-modified', 'name']:
                sort = 'name'
        queryset = queryset.filter(created_by=self.request.user).order_by(sort)
        return super().filter_queryset(queryset)
