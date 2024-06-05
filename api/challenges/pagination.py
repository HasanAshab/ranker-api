from django.db import models
from rest_framework.pagination import (
    LimitOffsetPagination,
)
from drf_pagination_meta_wrap.mixins import WrapPaginationMetadataMixin
from .serializers import (
    ChallengeDifficultyCountSerializer,
)


class ChallengePagination(WrapPaginationMetadataMixin, LimitOffsetPagination):
    def get_additional_metadata(self):
        from api.difficulties.models import Difficulty
        from .models import Challenge

        difficulties_queryset = Difficulty.objects.filter(
            challenge__user=self.request.user,
            challenge__status=Challenge.Status.ACTIVE,
        ).annotate(count=models.Count("challenge"))

        difficulties = ChallengeDifficultyCountSerializer(
            difficulties_queryset, many=True
        ).data
        print(difficulties)

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
