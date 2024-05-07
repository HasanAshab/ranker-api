from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import RecentUserSearch
from .serializers import ListRecentUserSearchSerializer
from .pagination import RecentUserSearchPagination


from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class BulkDestroyAPIView(GenericAPIView):
    def perform_destroy(self, queryset):
        queryset.delete()

    def delete(self, request):
        self.perform_destroy(self.get_queryset())
        return Response(status=204)


class ListDestroyAPIView(ListAPIView):
    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request):
        for insance in self.get_queryset():
            self.perform_destroy(insance)
        return Response(status=204)


class ListBulkDestroyAPIView(ListAPIView, BulkDestroyAPIView):
    pass


class RecentUserSearchesView(ListBulkDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = RecentUserSearch.objects.none()
    serializer_class = ListRecentUserSearchSerializer
    pagination_class = RecentUserSearchPagination

    def get_queryset(self):
        return self.request.user.searches.all()


class RecentUserSearchView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.searches.all()
