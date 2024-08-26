from django.conf import settings
from django.db import models


class RecentUserSearch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="searches",
    )
    searched_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="searchers",
    )

    searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} searched for {self.searched_user}"

    class Meta:
        ordering = ["-searched"]
