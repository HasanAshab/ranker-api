from rest_framework import serializers


class LoginTokenSSESerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)


class TokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)
