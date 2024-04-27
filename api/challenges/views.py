from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ListChallengeSerializer, ChallengeSerializer
from .pagination import ChallengeCursorPagination


class ChallengesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListChallengeSerializer
    pagination_class = ChallengeCursorPagination

    def get_queryset(self):

        return self.request.user.challenge_set.exclude(is_completed=True).prefetch_related('difficulty')


class ChallengesActivityView(APIView):
    def get(self, request):
        completed_challenges = self.request.user.challenge_set.filter(
            is_completed=True
        )
        # serial


class ChallengeView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return self.request.user.challenge_set.exclude(is_completed=True)
