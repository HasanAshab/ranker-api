from rest_framework import serializers
from api.level_titles.models import LevelTitle
from api.level_titles.serializers import LevelTitleSerializer


class UserLevelTitleMixin(metaclass=serializers.SerializerMetaclass):
    level_title = serializers.SerializerMethodField()

    def get_level_title(self, user):
        level_title = LevelTitle.objects.get_for_user(user)
        return LevelTitleSerializer(level_title).data
