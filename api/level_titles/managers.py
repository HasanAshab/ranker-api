from django.db import models


class LevelTitleManager(models.Manager):
    def get_for_user(self, user):
        status = (
            self.filter(required_level__lte=user.level)
            .order_by("-required_level")
            .first()
        )
        if not status:
            raise Exception(f"No title exists for level: {user.level}")
        return status
