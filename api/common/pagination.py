from rest_framework import pagination
from drf_pagination_meta_wrap.mixins import (
    WrapPaginationMetadataMixin,
)


class BasePagination(pagination.BasePagination):
    page_size_query_param = "page_size"
    page_size = 15


class PageNumberPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    pagination.PageNumberPagination,
):
    pass


class LimitOffsetPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    pagination.LimitOffsetPagination,
):
    pass


class CursorPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    pagination.CursorPagination,
):
    pass
