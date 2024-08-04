from django.core.signing import BadSignature, SignatureExpired
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .utils import login_using_token


class TokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        fields = ("token",)

    def validate(self, data):
        try:
            _, api_token = login_using_token(data["token"])
            return api_token
        except (BadSignature, SignatureExpired):
            raise ValidationError("Invalid token.")
