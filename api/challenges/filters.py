from django_filters import rest_framework as filters
from .models import Challenge


class ChallengeFilter(filters.FilterSet):
    due_date = filters.BooleanFilter(method="filter_due_date")

    class Meta:
        model = Challenge
        fields = ("difficulty", "is_pinned", "due_date")

    def filter_due_date(self, queryset, name, value):
        return queryset.exclude(due_date__isnull=value)
