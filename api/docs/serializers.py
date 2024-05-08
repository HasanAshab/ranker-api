from rest_framework import serializers


class StandardResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()

    class Meta:
        should_standardize_schema = False
