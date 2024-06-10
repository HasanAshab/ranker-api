from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer


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
