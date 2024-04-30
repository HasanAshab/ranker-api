from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from rest_framework import filters
from rest_framework.settings import api_settings


class MultiFieldOrderingFilter(filters.BaseFilterBackend):
    ordering_param = api_settings.ORDERING_PARAM
    ordering_description = _(
        "Which strategy to use when ordering the results."
    )

    def get_default_ordering(self, view):
        order = getattr(view, "ordering", None)
        if order:
            return getattr(view, "order_set", {}).get(order)

    def get_ordering(self, request, queryset, view):
        order = request.query_params.get(self.ordering_param)
        if order:
            ordering = getattr(view, "order_set", {}).get(order)
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_schema_operation_parameters(self, view):
        available_orders = list(getattr(view, "order_set", {}).keys())
        return [
            {
                "name": self.ordering_param,
                "required": False,
                "in": "query",
                "description": force_str(self.ordering_description),
                "schema": {
                    "type": "string",
                    "enum": available_orders,
                    "example": available_orders[0],
                },
            },
        ]
