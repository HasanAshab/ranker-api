from drf_spectacular.utils import OpenApiResponse
from api.docs.serializers import SuccessfulApiResponseSerializer


class SuccessfulApiResponse(OpenApiResponse):
    def __init__(self, description=None, examples=None):
        super().__init__(
            response=SuccessfulApiResponseSerializer,
            description=description,
            examples=examples,
        )
