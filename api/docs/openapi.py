from drf_spectacular.openapi import AutoSchema as BaseAutoSchema
from drf_spectacular.utils import OpenApiResponse


class AutoSchema(BaseAutoSchema):
    def _get_response_for_code(
        self, serializer, status_code, media_types=None, direction="response"
    ):
        response = super()._get_response_for_code(
            serializer, status_code, media_types, direction
        )
        schema_ref = response["content"]["application/json"]["schema"]["$ref"]
        if isinstance(serializer, OpenApiResponse):
            serializer = serializer.response

        if not getattr(
            serializer,
            "should_format",
            not schema_ref.startswith("#/components/schemas/Paginated"),
        ):
            return response
        schema = self._format_response_schema(schema_ref)
        response["content"]["application/json"]["schema"] = schema
        return response

    def _format_response_schema(self, schema_ref):
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "data": {"$ref": schema_ref},
            },
        }
