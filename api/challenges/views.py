from django.db.models import F, Count
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
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
    filterset_class = ChallengeFilter
    queryset = Challenge.objects.none()

    def get_queryset(self):
        return Challenge.objects.filter(
            user=self.request.user,
            is_completed=False,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChallengeView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return Challenge.objects.filter(
            user=self.request.user,
            is_completed=False,
        )


class ChallengeActivitiesView(ListAPIView):
    serializer_class = ChallengeActivitiesSerializer
    queryset = Challenge.objects.none()

    def get_queryset(self):
        return (
            Challenge.objects.filter(user=self.request.user, is_completed=True)
            .values("difficulty__id", "difficulty__name")
            .annotate(
                id=F("difficulty__id"),
                name=F("difficulty__name"),
                count=Count("id"),
            )
        )
