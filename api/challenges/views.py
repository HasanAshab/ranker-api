from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import filters
from .models import Challenge
from .filters import ChallengeFilter
from .serializers import (
    ListChallengeSerializer,
    ChallengeSerializer,
    ChallengeActivitiesSerializer,
)
from .pagination import ChallengeCursorPagination


class ChallengesView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListChallengeSerializer
    pagination_class = ChallengeCursorPagination
    queryset = Challenge.objects.none()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # search_fields = ("@title", "@description")
    search_fields = ("title", "description")
    filterset_class = ChallengeFilter
    ordering_fields = ("-is_pinned", "-id", "difficulty")
    ordering = ("-is_pinned", "-id")

    def get_queryset(self):
        return Challenge.objects.active().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChallengeView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return Challenge.objects.active().filter(user=self.request.user)


class ChallengeActivitiesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeActivitiesSerializer
    queryset = Challenge.objects.none()

    def get_queryset(self):
        return Challenge.objects.activities(user=self.request.user)
