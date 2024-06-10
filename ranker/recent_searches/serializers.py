from rest_framework import serializers
from ranker.users.serializers import UserDetailsSerializer
from .models import RecentUserSearch


class RecentUserSearchListSerializer(serializers.ModelSerializer):
    searched_user = UserDetailsSerializer()

    class Meta:
        model = RecentUserSearch
        fields = (
            "id",
            "searched_user",
        )
