from django.db import models
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
    ChallengeDifficultySerializer,
)
from .pagination import ChallengeCursorPagination


class MultiFieldOrderingFilter(filters.OrderingFilter):
    def get_ordering_fields(self, view, ordering):
        return getattr(view, 'order_set', {}).get(ordering)

    def get_default_ordering(self, view):
        ordering = getattr(view, 'ordering', None)
        if ordering:
            return self.get_ordering_fields(view, ordering)

    def get_ordering(self, request, queryset, view):
        ordering = request.query_params.get(self.ordering_param)
        if ordering:
            fields = self.get_ordering_fields(view, ordering)
            if fields:
                return fields
        return self.get_default_ordering(view)
    
class ChallengesView(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = ListChallengeSerializer
    #pagination_class = ChallengeCursorPagination
    queryset = Challenge.objects.none()
    filter_backends = (filters.SearchFilter, MultiFieldOrderingFilter)
    # search_fields = ("@title", "@description")
    search_fields = ("title", "description")
    filterset_class = ChallengeFilter
    ordering = "ordered"
    order_set = {
        'ordered': ('-is_pinned', '-id'),
        'difficulty': ('difficulty__points', '-is_pinned', '-id'),
    }
    
    def get_queryset(self):
        return Challenge.objects.all()#self.request.user.challenge_set.active()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChallengeView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return self.request.user.challenge_set.active().filter()


class ChallengeActivitiesView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: ChallengeActivitiesSerializer,
        }
    )
    def get(self, request):
        totals = self.request.user.challenge_set.aggregate(
            submitted=models.Count("id"),
            completed=models.Count(
                models.Case(
                    models.When(
                        status=Challenge.Status.COMPLETED, then=models.Value(1)
                    ),
                    output_field=models.IntegerField(),
                )
            ),
            failed=models.Count(
                models.Case(
                    models.When(
                        status=Challenge.Status.FAILED, then=models.Value(1)
                    ),
                    output_field=models.IntegerField(),
                )
            ),
        )
        challenge_activities = {
            "total": totals["submitted"],
            "failed": totals["failed"],
            "completed": {
                "total": totals["completed"],
            },
        }
        difficulties_queryset = (
            self.request.user.challenge_set.completed()
            .values("difficulty__id")
            .annotate(
                count=models.Count("id"),
            )
        )
        difficulties = ChallengeDifficultySerializer(
            difficulties_queryset, many=True
        ).data
        challenge_activities["completed"]["difficulties"] = difficulties
        return Response(challenge_activities)
