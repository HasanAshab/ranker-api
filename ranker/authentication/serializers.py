from rest_framework import serializers


class TokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)
