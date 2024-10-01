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
        difficulties_queryset = (
            Difficulty.objects.with_challenge_count().filter(
                challenge__user=self.request.user,
                challenge__status=Challenge.Status.ACTIVE,
            )
        )

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
