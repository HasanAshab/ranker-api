from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer
from api.level_titles.models import LevelTitle
from api.level_titles.serializers import LevelTitleSerializer


class UserAvatarLinkSerializerMixin(metaclass=serializers.SerializerMetaclass):
    links = serializers.SerializerMethodField()

    @extend_schema_field(
        inline_serializer(
            name="UserAvatarLink",
            fields={
                "avatar": serializers.URLField(allow_null=True),
            },
        )
    )
    def get_links(self, user):
        return {
            "avatar": user.avatar if user.avatar else None,
        }


class UserLevelTitleMixin(metaclass=serializers.SerializerMetaclass):
    level_title = serializers.SerializerMethodField()

    @extend_schema_field(LevelTitleSerializer)
    def get_level_title(self, user):
        level_title = LevelTitle.objects.get_for_user(user)
        return LevelTitleSerializer(level_title).data
