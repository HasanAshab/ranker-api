from rest_framework import serializers
from api.users.serializers import ListUserSerializer
from .models import RecentUserSearch


class ListRecentUserSearchSerializer(serializers.ModelSerializer):
    searched_user = ListUserSerializer()

    class Meta:
        model = RecentUserSearch
        fields = "__all__"
