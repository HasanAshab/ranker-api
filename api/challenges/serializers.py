from rest_framework import serializers
from .models import Challenge, ChallengeStep


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = (
            "id",
            "title",
            "status",
            "is_pinned",
            "due_date",
            "difficulty",
            "order",
        )


class ChallengeDifficultySerializer(serializers.Serializer):
    id = serializers.IntegerField(source="difficulty__id")
    count = serializers.IntegerField()


class CompletedChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    difficulties = ChallengeDifficultySerializer(many=True)


class ChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    failed = serializers.IntegerField()
    completed = CompletedChallengeActivitiesSerializer()


class ReOrderingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField(min_value=0)


class ChallengeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeStep
        fields = (
            "id",
            "title",
            "is_completed",
            "order",
        )
