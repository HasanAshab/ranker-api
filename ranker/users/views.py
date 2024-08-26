from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework import filters
from .models import User
from .permissions import DeleteUserPermission
from .serializers import (
    UserListSerializer,
    UserDetailsSerializer,
)
from .pagination import UserCursorPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all().select_related("level_title")
    serializer_class = UserListSerializer
    pagination_class = UserCursorPagination
    # search_fields = ("@username", "@name")
    search_fields = ("username", "name")


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all().select_related("level_title")
    lookup_field = "username"
    serializer_class = UserDetailsSerializer

    def get_object(self):
        user = super().get_object()
        source = self.request.query_params.get("source")
        if source == "search" and self.request.user != user:
            self.request.user.searches.update_or_create(searched_user=user)
        return user
