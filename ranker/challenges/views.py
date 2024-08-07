from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status
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
from django_filters.rest_framework import DjangoFilterBackend
from drf_standardized_response.openapi.utils import standard_openapi_response
from ranker.difficulties.models import Difficulty
from .utils import generate_challenge_steps
from .models import Challenge, ChallengeStep
from .filters import ChallengeFilter
from .serializers import (
    ChallengeSerializer,
    ChallengeActivitiesSerializer,
    ChallengeDifficultyCountSerializer,
    ReOrderingSerializer,
    ChallengeStepSerializer,
)
from .pagination import ChallengePagination


class ChallengesView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer
    pagination_class = ChallengePagination
    queryset = Challenge.objects.none()
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
    )
    # search_fields = ("@title", "@description")
    search_fields = ("title", "steps__title")
    filterset_class = ChallengeFilter

    def get_queryset(self):
        return self.request.user.challenge_set.active().select_related(
            "difficulty"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChallengeView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        return self.request.user.challenge_set.active().select_related(
            "difficulty"
        )


class ChallengeActivitiesView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: ChallengeActivitiesSerializer,
        }
    )
    def get(self, request):
        count = self.request.user.challenge_set.aggregate(
            total=models.Count("id"),
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
            "total": count["total"],
            "failed": count["failed"],
            "completed": {
                "total": count["completed"],
            },
        }

        difficulties_queryset = (
            Difficulty.objects.with_challenge_count().filter(
                challenge__user=self.request.user,
                challenge__status=Challenge.Status.COMPLETED,
            )
        )
        difficulties = ChallengeDifficultyCountSerializer(
            difficulties_queryset, many=True
        ).data

        challenge_activities["completed"]["difficulties"] = difficulties
        return Response(challenge_activities)


class ChallengeOrdersView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReOrderingSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        kwargs.setdefault("many", True)
        return serializer_class(*args, **kwargs)

    @extend_schema(
        responses={
            200: standard_openapi_response(),
        }
    )
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        challenges = []
        for challenge_order in serializer.validated_data:
            challenge = Challenge(
                id=challenge_order["id"],
                order=challenge_order["order"],
            )
            challenges.append(challenge)

        request.user.challenge_set.unpinned().active().bulk_update(
            challenges, ["order"]
        )

        return Response("Challenges reordered.")


class ChallengeStepsView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeStepSerializer
    queryset = ChallengeStep.objects.none()

    def get_queryset(self):
        challenge = get_object_or_404(
            self.request.user.challenge_set.active(),
            pk=self.kwargs["pk"],
        )
        return challenge.steps.all()

    def perform_create(self, serializer):
        challenge = get_object_or_404(
            self.request.user.challenge_set.active(),
            pk=self.kwargs["pk"],
        )
        serializer.save(challenge=challenge)


class ChallengeStepView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeStepSerializer
    queryset = ChallengeStep.objects.none()

    def get_queryset(self):
        challenge = get_object_or_404(
            self.request.user.challenge_set.active(),
            pk=self.kwargs["pk"],
        )
        return challenge.steps.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs["step_pk"],
        )


class ChallengeStepOrdersView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReOrderingSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("many", True)
        return self.serializer_class(*args, **kwargs)

    @extend_schema(
        responses={
            200: standard_openapi_response(),
        }
    )
    def patch(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        challenge = get_object_or_404(
            request.user.challenge_set.active(),
            pk=pk,
        )
        challenge_steps = []
        for challenge_step_order in serializer.validated_data:
            challenge_step = ChallengeStep(
                id=challenge_step_order["id"],
                order=challenge_step_order["order"],
            )
            challenge_steps.append(challenge_step)

        challenge.steps.bulk_update(challenge_steps, ["order"])

        return Response("Challenges steps reordered.")


class ChallengeStepsGenerationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        return None

    @extend_schema(
        responses={
            201: ChallengeStepSerializer(many=True),
        }
    )
    def post(self, request, pk):
        challenge = get_object_or_404(
            request.user.challenge_set.active(),
            pk=pk,
        )
        challenge_steps = generate_challenge_steps(challenge)
        serializer = ChallengeStepSerializer(challenge_steps, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
