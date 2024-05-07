from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


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
