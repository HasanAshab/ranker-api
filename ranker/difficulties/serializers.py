from rest_framework import serializers
from .models import Difficulty


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = "__all__"
