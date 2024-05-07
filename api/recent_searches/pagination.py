from api.common.pagination import (
    CursorPagination,
)


class RecentUserSearchCursorPagination(CursorPagination):
    ordering = ("-searched_at", "-id")
