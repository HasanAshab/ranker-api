from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import filters
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
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


class ChallengeActivitiesView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: ChallengeActivitiesSerializer,
        }
    )
    def get(self, request):
        challenge_activities = Challenge.objects.activities(user=request.user)
        return Response(challenge_activities)
