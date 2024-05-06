from api.docs.utils import to_openapi_schema


class WrapPaginationMetadataMixin:
    paginated_response_data_key = "results"
    paginated_response_meta_key = "meta"
    additional_metadata = {}

    def get_additional_metadata(self):
        return self.additional_metadata

    def get_paginated_response(self, data):
        data_key = self.paginated_response_data_key
        meta_key = self.paginated_response_meta_key
        response = super().get_paginated_response(data)
        data = response.data.pop(data_key)
        response.data = {
            meta_key: {
                **response.data,
                **self.get_additional_metadata(),
            },
            data_key: data,
        }
        return response

    def get_additional_metadata_properties_schema(self):
        properties = {}
        additional_metadata = self.get_additional_metadata()
        for key, value in additional_metadata.items():
            properties[key] = to_openapi_schema(value)
        return properties

    def get_paginated_response_schema(self, schema):

        data_key = self.paginated_response_data_key
        meta_key = self.paginated_response_meta_key
        schema = super().get_paginated_response_schema(schema)
        data_schema = schema["properties"].pop(data_key)
        schema["properties"] = {
            meta_key: {
                "type": "object",
                "properties": {
                    **schema["properties"],
                    **self.get_additional_metadata_properties_schema(),
                },
            },
            data_key: data_schema,
        }
        return schema
