from django.db import models
from rest_framework.pagination import (
    LimitOffsetPagination,
)
from drf_pagination_meta_wrap.mixins import WrapPaginationMetadataMixin
from .serializers import (
    ChallengeDifficultySerializer,
)


class ChallengePagination(WrapPaginationMetadataMixin, LimitOffsetPagination):
    def get_additional_metadata(self):
        difficulties_queryset = (
            self.request.user.challenge_set.active()
            .values("difficulty__id")
            .annotate(
                count=models.Count("id"),
            )
        )

        difficulties = ChallengeDifficultySerializer(
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
                        "count": {"type": "integer"},
                    },
                },
            }
        }
