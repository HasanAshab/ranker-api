from drf_spectacular.utils import OpenApiResponse, inline_serializer
from .serializers import SuccessfulApiResponse


def to_openapi_type(python_type):
    type_mapping = {
        int: "integer",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "array",
    }
    return type_mapping.get(python_type, "unknown")


def to_openapi_schema(input):
    if isinstance(input, dict):
        return {
            "type": "object",
            "properties": {k: to_openapi_schema(v) for k, v in input.items()},
            "required": list(input.keys()),
        }
    elif isinstance(input, list):
        return {
            "type": "array",
            "items": to_openapi_schema(input[0]) if input else {},
        }
    else:
        return {"type": to_openapi_type(type(input))}


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
