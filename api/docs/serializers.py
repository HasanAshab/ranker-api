from rest_framework import serializers


class SuccessfulApiResponse(serializers.Serializer):
    should_format = False
    success = serializers.BooleanField()
    message = serializers.CharField()
