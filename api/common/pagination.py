from rest_framework import pagination
from .response import ImmutableResponse


class BasePagination(pagination.BasePagination):
    page_size_query_param = "page_size"
    page_size = 15


class PageNumberPagination(BasePagination, pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return ImmutableResponse(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class LimitOffsetPagination(BasePagination, pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return ImmutableResponse(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class CursorPagination(BasePagination, pagination.CursorPagination):
    def get_paginated_response(self, data):
        return ImmutableResponse(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
