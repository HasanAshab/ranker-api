from rest_framework import pagination
from .mixins import (
    ImmutablePaginationResponseMixin,
    WrapPaginationMetadataMixin,
)


class BasePagination(pagination.BasePagination):
    page_size_query_param = "page_size"
    page_size = 15


class PageNumberPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    ImmutablePaginationResponseMixin,
    pagination.PageNumberPagination,
):
    pass


class LimitOffsetPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    ImmutablePaginationResponseMixin,
    pagination.LimitOffsetPagination,
):
    pass


class CursorPagination(
    BasePagination,
    WrapPaginationMetadataMixin,
    ImmutablePaginationResponseMixin,
    pagination.CursorPagination,
):
    pass
