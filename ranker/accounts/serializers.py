import re
from django.conf import settings
from rest_framework import serializers
from ranker.common.utils import (
    twilio_verification,
)
from ranker.users.models import User
from ranker.users.mixins import UserAvatarLinkSerializerMixin
from ranker.level_titles.serializers import LevelTitleSerializer


class ProfileSerializer(
    UserAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    level_title = LevelTitleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_email_verified",
            "username",
            "name",
            "gender",
            "phone_number",
            "avatar",
            "date_joined",
            "is_superuser",
            "is_staff",
            "total_xp",
            "level",
            "level_title",
            "rank",
            "links",
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "phone_number",
            "total_xp",
            "rank",
        )
        extra_kwargs = {"avatar": {"write_only": True}}


class SuggestUsernameSerializer(serializers.Serializer):
    prefix = serializers.CharField(required=False)
    max_suggestions = serializers.IntegerField(
        max_value=settings.USERNAME_MAX_SUGGESTIONS,
        default=settings.USERNAME_MAX_SUGGESTIONS,
    )

    def clean_prefix(self, prefix):
        return re.sub(r"[^a-zA-Z0-9@/.\+\-_]", "", prefix)


class PhoneNumberSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("phone_number", "otp")
        extra_kwargs = {"phone_number": {"required": True}}

    def validate_phone_number(self, phone_number):
        if phone_number == self.instance.phone_number:
            msg = "Phone number can't be same as old one."
            raise serializers.ValidationError(msg)
        return phone_number

    def validate_otp(self, otp):
        phone_number = self.initial_data["phone_number"]
        if not twilio_verification.is_valid(phone_number, otp):
            raise serializers.ValidationError("Invalid OTP code.")
        return otp

    def update(self, instance, validated_data):
        phone_number = validated_data.get("phone_number")
        otp = validated_data.get("otp")
        if not otp:
            twilio_verification.send_through_sms(phone_number)
            return instance
        instance.phone_number = phone_number
        instance.save()
        return instance
