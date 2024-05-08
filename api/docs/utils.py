from drf_spectacular.utils import OpenApiResponse
from .serializers import StandardResponseSerializer


def standard_openapi_response(
    name=None, fields=None, description="", examples=None, **kwargs
):
    if fields:
        if not name:
            raise ValueError("name is required if extra fields are provided")
        serializer = type(name, (StandardResponseSerializer,), fields)
    else:
        serializer = StandardResponseSerializer
    return OpenApiResponse(serializer(**kwargs), description, examples)
