from drf_standardized_errors.openapi import AutoSchema as BaseAutoSchema
from drf_spectacular.utils import OpenApiResponse


class AutoSchema(BaseAutoSchema):
    def _get_response_for_code(
        self, serializer, status_code, media_types=None, direction="response"
    ):
        response = super()._get_response_for_code(
            serializer, status_code, media_types, direction
        )

        if isinstance(serializer, OpenApiResponse):
            serializer = serializer.response

        if not (content := response.get("content")):

            return response
        if "application/json" not in content:
            return response

        schema = content["application/json"]["schema"]
        reference = schema.get("$ref", schema.get("items", {}).get("$ref"))
        if not reference:
            return response
        is_paginated_response = reference.startswith(
            "#/components/schemas/Paginated"
        )
        is_error_response = "ErrorResponse" in reference

        if not getattr(
            serializer,
            "should_format",
            not (is_paginated_response or is_error_response),
        ):
            return response

        formatted_schema = self.format_response_schema(schema)
        content["application/json"]["schema"] = formatted_schema
        return response

    def format_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "data": schema,
            },
        }
