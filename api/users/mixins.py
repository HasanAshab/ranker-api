from rest_framework import serializers
from api.statuses.models import Status
from api.statuses.serializers import StatusSerializer


class UserStatusMixin(metaclass=serializers.SerializerMetaclass):
    status = serializers.SerializerMethodField()

    def get_status(self, user):
        status = Status.objects.get_for_user(user)
        return StatusSerializer(status).data
