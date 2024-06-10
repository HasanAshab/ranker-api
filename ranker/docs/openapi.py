from drf_standardized_errors.openapi import AutoSchema as ErrorAutoSchema
from drf_standardized_response.openapi import StandardizedSchemaMixin


class AutoSchema(StandardizedSchemaMixin, ErrorAutoSchema):
    pass
