import django_filters

from .models import Folder, Bookmark


class FolderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',)

    class Meta:
        model = Folder
        fields = ['name']

    sort = django_filters.OrderingFilter(
        choices=(
            ('name', 'Name'),
            ('-modified', 'Modified(descending)'),
            ('-created', 'Created(descending)'),
        ),
    )

    def filter_queryset(self, queryset):
        queryset = queryset.filter(created_by=self.request.user)
        return super().filter_queryset(queryset)


class BookmarkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Bookmark
        fields = ['name']

    def filter_queryset(self, queryset):
        sort = 'name'
        try:
            folder = Folder.objects.get(created_by=self.request.user, slug=self.request.path.split('/')[2])
        except Folder.DoesNotExist:
            folder = None
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-created', '-modified', 'name']:
                sort = 'name'
        if folder is None:
            queryset = queryset.filter(created_by=self.request.user).order_by(sort)
        else:
            queryset = queryset.filter(created_by=self.request.user, folder=folder).order_by(sort)
        return super().filter_queryset(queryset)
