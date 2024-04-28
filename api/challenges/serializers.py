from rest_framework import serializers
from .models import Challenge


class ListChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        exclude = ("description", "user")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        exclude = ("user",)


class ChallengeActivitiesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    count = serializers.IntegerField()
