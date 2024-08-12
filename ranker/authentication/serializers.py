from django.core.signing import BadSignature, SignatureExpired
from rest_framework import serializers
from .utils import login_using_token


class LoginTokenSSESerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)


class TokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)

    def validate_token(self, value):
        try:
            _, api_token = login_using_token(value)
            return api_token
        except SignatureExpired:
            raise serializers.ValidationError(
                "Token expired.", code="token_expired"
            )
        except BadSignature:
            raise serializers.ValidationError(
                "Invalid token.", code="invalid_token"
            )
