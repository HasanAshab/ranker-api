from django.db import models
from django.utils import timezone
from rest_framework.pagination import (
    LimitOffsetPagination,
)
from drf_pagination_meta_wrap.mixins import WrapPaginationMetadataMixin
from ranker.difficulties.models import Difficulty
from .models import Challenge
from .serializers import (
    ChallengeDifficultyCountSerializer,
)


class ChallengePagination(WrapPaginationMetadataMixin, LimitOffsetPagination):
    def get_additional_metadata(self):
        difficulties_queryset = Difficulty.objects.annotate(
            challenge_count=models.Count(
                "challenge",
                filter=(
                    models.Q(challenge__user=self.request.user)
                    & models.Q(challenge__status=Challenge.Status.ACTIVE)
                    & (
                        models.Q(challenge__due_date__isnull=True)
                        | models.Q(challenge__due_date__gt=timezone.now())
                    )
                ),
            )
        ).filter(challenge_count__gt=0)

        difficulties = ChallengeDifficultyCountSerializer(
            difficulties_queryset, many=True
        ).data

        return {"difficulties": difficulties}

    def get_additional_metadata_properties_schema(self):
        return {
            "difficulties": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "challenge_count": {"type": "integer"},
                        "name": {"type": "string"},
                        "slug": {"type": "string"},
                        "light_color": {"type": "string"},
                        "dark_color": {"type": "string"},
                        "xp_value": {"type": "integer"},
                        "xp_penalty": {"type": "integer"},
                    },
                },
            }
        }
