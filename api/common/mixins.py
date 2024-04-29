from .response import ImmutableResponse


class WrapPaginationMetadataMixin:
    paginated_response_data_key = "results"
    paginated_response_meta_key = "meta"

    def get_paginated_response(self, data):
        data_key = self.paginated_response_data_key
        meta_key = self.paginated_response_meta_key
        response = super().get_paginated_response(data)
        data = response.data.pop(data_key)
        response.data = {
            meta_key: response.data,
            data_key: data,
        }
        return response

    def get_paginated_response_schema(self, schema):
        data_key = self.paginated_response_data_key
        meta_key = self.paginated_response_meta_key
        schema = super().get_paginated_response_schema(schema)
        data_schema = schema["properties"].pop(data_key)
        schema["properties"] = {
            meta_key: {
                "type": "object",
                "properties": schema["properties"],
            },
            data_key: data_schema,
        }

        print(schema)
        return schema


class ImmutablePaginationResponseMixin:
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        return ImmutableResponse(response.data)
