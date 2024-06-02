from rest_framework import serializers
from .models import LevelTitle


class LevelTitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTitle
        fields = "__all__"


class LevelTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTitle
        exclude = ("required_level",)
