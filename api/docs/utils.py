from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, inline_serializer


i = 0
def successful_api_response(
    fields={},
    description='',
    examples=None
):
    global i
    i += 1
    serializer = inline_serializer(f'SuccessfulApiResponse{i}', {
        'should_format': False,
        'success': serializers.BooleanField(),
        'message': serializers.CharField(),
        **fields,
    })
    
    return OpenApiResponse(serializer, description, examples)
