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
        challenge_activities = {
            "total": self.filter(user=user).count(),
            "failed": self.failed().filter(user=user).count(),
        }

        completed_activities = {
            "total": self.completed().filter(user=user).count(),
            "difficulties": (
                self.completed()
                .filter(user=user)
                .values("difficulty__id", "difficulty__name")
                .annotate(
                    id=models.F("difficulty__id"),
                    name=models.F("difficulty__name"),
                    count=models.Count("id"),
                )
            ),
        }

        challenge_activities["completed"] = completed_activities

        return challenge_activities
