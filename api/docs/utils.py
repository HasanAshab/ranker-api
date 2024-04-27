from drf_spectacular.utils import OpenApiResponse, inline_serializer
from .serializers import SuccessfulApiResponse


def successful_api_response(
    fields=None, name=None, description="", examples=None
):
    if fields:
        if not name:
            raise ValueError("name is required if fields is provided")
        serializer = inline_serializer(
            name,
            {
                "should_format": False,
                **SuccessfulApiResponse._declared_fields,
                **fields,
            },
        )
    else:
        serializer = SuccessfulApiResponse

    return OpenApiResponse(serializer, description, examples)
