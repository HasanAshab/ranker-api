from django.db import models


class LevelTitleManager(models.Manager):
    def get_for_level(self, level):
        return self.filter(required_level__lte=level)

    def get_for_user(self, user):
        return self.get_for_level(user.level)
