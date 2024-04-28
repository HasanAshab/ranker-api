from api.common.pagination import (
    CursorPagination,
)


class ChallengeCursorPagination(CursorPagination):
    # ordering = "id"

    def get_ordering(self, request, queryset, view):
        ordering = ["-is_pinned", "-id"]
        if sort_by := request.query_params.get("sort_by"):
            ordering.insert(1, "-" + sort_by)
        print(ordering)
        return ordering
