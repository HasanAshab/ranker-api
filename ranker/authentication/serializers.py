from rest_framework import serializers
from ranker.users.models import User


class DifficultySerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "token")
