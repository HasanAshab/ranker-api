from django.utils import timezone
from django.db import models


class ChallengeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def inactive(self):
        return self.exclude(status=self.model.Status.ACTIVE)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def failed(self):
        return self.filter(status=self.model.Status.FAILED)

    def pinned(self):
        return self.filter(is_pinned=True)

    def unpinned(self):
        return self.filter(is_pinned=False)

    def repeated(self, repeat_type=None):
        if repeat_type is None:
            return self.exclude(repeat_type=self.model.RepeatType.ONCE)
        return self.filter(repeat_type=repeat_type)

    def daily(self):
        return self.filter(repeat_type=self.model.RepeatType.DAILY)

    def weekly(self):
        return self.filter(repeat_type=self.model.RepeatType.WEEKLY)

    def monthly(self):
        return self.filter(repeat_type=self.model.RepeatType.MONTHLY)

    def expired(self):
        return self.filter(due_date__lt=timezone.now())

    def unexpired(self):
        return self.filter(
            models.Q(due_date__isnull=True)
            | models.Q(due_date__gt=timezone.now())
        )

    def mark_as_active(self):
        return self.update(status=self.model.Status.ACTIVE)

    def mark_as_completed(self):
        return self.update(status=self.model.Status.COMPLETED)

    def mark_as_failed(self):
        return self.update(status=self.model.Status.FAILED)


class ChallengeStepQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(is_completed=True)

    def active(self):
        return self.filter(is_completed=False)
