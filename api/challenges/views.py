from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from .models import Challenge
from .filters import ChallengeFilter
from .serializers import ListChallengeSerializer, ChallengeSerializer
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


from django.db.models import Count


class ChallengeActivitiesView(APIView):
    def get(self, request):
        completed_counts = (
            Challenge.objects.filter(user=self.request.user, is_completed=True)
            .values("difficulty__id", "difficulty__name")
            .annotate(count=Count("id"))
        )
        print(list(completed_counts))

        response_data = [
            {
                "id": difficulty["difficulty__id"],
                "name": difficulty["difficulty__name"],
                "count": difficulty["count"],
            }
            for difficulty in completed_counts
        ]
        return Response(response_data)
