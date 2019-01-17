import django_filters

from .models import Folder


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
