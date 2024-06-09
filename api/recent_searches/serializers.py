from rest_framework import serializers
from api.users.serializers import UserDetailsSerializer
from .models import RecentUserSearch


class RecentUserSearchListSerializer(serializers.ModelSerializer):
    searched_user = UserDetailsSerializer()

    class Meta:
        model = RecentUserSearch
        fields = (
            "id",
            "searched_user",
        )
