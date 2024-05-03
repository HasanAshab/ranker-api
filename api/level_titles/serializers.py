from rest_framework import serializers
from .models import LevelTitle


class LevelTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTitle
        exclude = ("required_level",)
