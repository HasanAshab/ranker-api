from django.db import models


class DifficultyQuerySet(models.QuerySet):
    def with_challenge_count(self):
        return self.annotate(challenge_count=models.Count("challenge"))
