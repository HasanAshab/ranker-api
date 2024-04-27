from api.common.pagination import (
    CursorPagination,
)


class ChallengeCursorPagination(CursorPagination):
    ordering = "id"
