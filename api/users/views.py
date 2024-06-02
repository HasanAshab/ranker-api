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
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = UserCursorPagination
    # search_fields = ("@username", "@name")
    search_fields = ("username", "name")


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        is_search = request.query_params.get("is_search")
        if is_search == "true" and request.user != user:
            request.user.searches.update_or_create(searched_user=user)

        return super().retrieve(request, *args, **kwargs)
