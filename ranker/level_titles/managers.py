from django.db import models


class LevelTitleManager(models.Manager):
    def get_next(self, level_title):
        return self.filter(
            required_level__gt=level_title.required_level
        ).first()

    def get_previous(self, level_title):
        return self.filter(
            required_level__lt=level_title.required_level
        ).first()

    def get_for_level(self, level):
        return self.filter(required_level__lte=level).first()

    def get_for_user(self, user):
        return self.get_for_level(user.level)
