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


class CompletedChallengeDifficultySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    count = serializers.IntegerField()


class CompletedChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    difficulties = CompletedChallengeDifficultySerializer(many=True)


class ChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    failed = serializers.IntegerField()
    completed = CompletedChallengeActivitiesSerializer()
