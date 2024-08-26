from django.urls import reverse
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer
from ranker.level_titles.serializers import LevelTitleSerializer
from .models import User
from .mixins import UserAvatarLinkSerializerMixin


class UserListSerializer(
    UserAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    level_title = LevelTitleSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "level",
            "level_title",
            "links",
        )

    @extend_schema_field(
        inline_serializer(
            name="UserListLinks",
            fields={
                "self": serializers.URLField(),
                "avatar": serializers.URLField(allow_null=True),
            },
        )
    )
    def get_links(self, user):
        request = self.context["request"]
        profile_url = reverse(
            "user_details", kwargs={"username": user.username}
        )

        if "search" in request.query_params:
            return profile_url + "?source=search"

        return {
            **super().get_links(user),
            "self": profile_url,
        }


class UserDetailsSerializer(
    UserAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    level_title = LevelTitleSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "gender",
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
