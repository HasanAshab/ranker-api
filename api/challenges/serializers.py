from rest_framework import serializers
from api.difficulties.serializers import DifficultySerializer
from .models import Challenge


class ListChallengeSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer()

    class Meta:
        model = Challenge
        exclude = ("description", "user")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        exclude = ("user",)
