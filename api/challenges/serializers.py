from rest_framework import serializers
from .models import Challenge, ChallengeStep
from api.difficulties.models import Difficulty


class ChallengeDifficultySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Difficulty
        fields = "__all__"
        read_only_fields = (
            "name",
            "slug",
            "xp_value",
            "light_color",
            "dark_color",
        )


class ChallengeSerializer(serializers.ModelSerializer):
    difficulty = ChallengeDifficultySerializer()

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

    def update(self, instance, validated_data):
        difficulty_id = validated_data.pop("difficulty", {}).get("id")
        if difficulty_id:
            instance.difficulty_id = difficulty_id

        return super().update(instance, validated_data)


class ChallengeDifficultyCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()

    class Meta:
        model = Difficulty
        fields = ("count", "slug")


class CompletedChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    difficulties = ChallengeDifficultyCountSerializer(many=True)


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
