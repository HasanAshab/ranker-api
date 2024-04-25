from api.common.pagination import (
    CursorPagination,
)


class UserCursorPagination(CursorPagination):
    ordering = "date_joined"
