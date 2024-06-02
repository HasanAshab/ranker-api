from rest_framework import serializers
from api.users.serializers import UserListSerializer
from .models import RecentUserSearch


class RecentUserSearchListSerializer(serializers.ModelSerializer):
    searched_user = UserListSerializer()

    class Meta:
        model = RecentUserSearch
        fields = "__all__"
