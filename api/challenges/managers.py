from django.db import models


class ChallengeManager(models.Manager):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def failed(self):
        return self.filter(status=self.model.Status.FAILED)

    def pinned(self):
        return self.filter(is_pinned=True)

    def activities(self, user):
        return (
            self.completed()
            .filter(user=user)
            .values("difficulty__id", "difficulty__name")
            .annotate(
                id=models.F("difficulty__id"),
                name=models.F("difficulty__name"),
                count=models.Count("id"),
            )
        )
