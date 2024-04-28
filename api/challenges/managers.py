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
