from django.db import models


class StatusManager(models.Manager):
    def get_for_user(self, user):
        return self.filter(required_level__lte=user.level).order_by('-required_level').first()
