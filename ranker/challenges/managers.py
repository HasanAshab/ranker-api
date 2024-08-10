from django.db import models
from .querysets import ChallengeStepQuerySet


class ChallengeStepManager(models.Manager):
    def get_queryset(self):
        return ChallengeStepQuerySet(self.model, using=self._db)

    def mark_as_completed(self):
        return self.update(is_completed=True)
