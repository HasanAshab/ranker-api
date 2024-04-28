from drf_spectacular.openapi import AutoSchema as BaseAutoSchema
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

        if not getattr(
            serializer,
            "should_format",
            not schema.get("$ref", "").startswith(
                "#/components/schemas/Paginated"
            ),
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
