from django.utils.translation import gettext_lazy as _
from django.db import models
from django_filters import rest_framework as filters
from .models import Challenge


class ChallengeFilter(filters.FilterSet):
    due_date = filters.BooleanFilter(method="filter_due_date")
    ordering = filters.ChoiceFilter(
        method="ordering_queryset",
        choices=(
            ("ordered", _("Ordered")),
            ("difficulty", _("Difficulty")),
        ),
    )

    class Meta:
        model = Challenge
        fields = ("difficulty", "is_pinned", "due_date")

    def filter_due_date(self, queryset, name, value):
        return queryset.exclude(due_date__isnull=value)

    def ordering_queryset(self, queryset, name, value):
        if value == "ordered":
            return queryset.order_by("order", "-id")
        elif value == "difficulty":
            return queryset.order_by(
                "-difficulty",
                "-is_pinned",
                models.F("due_date").asc(nulls_last=True),
                "-id",
            )
        return queryset
