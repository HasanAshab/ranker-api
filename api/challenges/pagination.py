from api.common.pagination import (
    CursorPagination,
)
from .models import Challenge

from django.db import models
from .serializers import (
    ChallengeDifficultySerializer,
)


class ChallengeCursorPagination(CursorPagination):
    ordering = "id"

    def get_additional_metadata(self):
        active_challenge_difficulties_queryset = (
            Challenge.objects.active()
            .filter(user=self.request.user)
            .values("difficulty__id")
            .annotate(
                count=models.Count("id"),
            )
        )

        active_challenge_difficulties = ChallengeDifficultySerializer(
            active_challenge_difficulties_queryset, many=True
        ).data

        total_active_challenges = sum(
            difficulty["count"] for difficulty in active_challenge_difficulties
        )

        return {
            "active_challenges": {
                "total": total_active_challenges,
                "difficulties": active_challenge_difficulties,
            }
        }

    def get_additional_metadata_properties_schema(self):
        return {
            "active_challenges": {
                "type": "object",
                "properties": {
                    "total": {"type": "integer"},
                    "difficulties": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "count": {"type": "integer"},
                            },
                        },
                    },
                },
            }
        }
