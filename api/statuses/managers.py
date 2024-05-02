from django.db import models


class StatusManager(models.Manager):
    def get_for_user(self, user):
        status = (
            self.filter(required_level__lte=user.level)
            .order_by("-required_level")
            .first()
        )
        if not status:
            raise Exception(
                f"""At least one status should be exist
                on database for level: {user.level}"""
            )
        return status
