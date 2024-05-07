from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.common.generics import ListBulkDestroyAPIView
from .models import RecentUserSearch
from .serializers import ListRecentUserSearchSerializer
from .pagination import RecentUserSearchPagination


@extend_schema_view(
    delete=extend_schema(
        operation_id="recent_searches_destroy_all",
    ),
)
class RecentUserSearchesView(ListBulkDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = RecentUserSearch.objects.none()
    serializer_class = ListRecentUserSearchSerializer
    pagination_class = RecentUserSearchPagination

    def get_queryset(self):
        return self.request.user.searches.all()


class RecentUserSearchView(DestroyAPIView):
    def get_serializer(self, *args, **kwargs):
        return None

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.searches.all()
