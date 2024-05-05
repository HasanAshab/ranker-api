from django.conf import settings
from django.utils import timezone
from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)

# from django.contrib.postgres.indexes import GinIndex
# from django.contrib.postgres.search import SearchVector, SearchVectorField
from datetime_validators.validators import date_time_is_future_validator
from .managers import ChallengeManager


class Challenge(models.Model):
    XP_PERCENTAGE_BONUS_FOR_DUE_DATE = 15

    def __str__(self):
        return self.title

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")

    title = models.CharField(
        _("Title"),
        max_length=50,
        help_text="Title of the challenge.",
    )
    description = models.TextField(
        _("Description"),
        max_length=200,
        blank=True,
        help_text="Description of the challenge.",
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status,
        default=Status.ACTIVE,
        help_text="Status of the challenge.",
    )
    is_pinned = models.BooleanField(
        _("Is Pinned"),
        default=False,
        help_text="Whether the challenge is pinned.",
    )
    due_date = models.DateTimeField(
        _("Due Date"),
        null=True,
        help_text="Due date of the challenge.",
        validators=[date_time_is_future_validator],
    )
    difficulty = models.ForeignKey(
        "difficulties.Difficulty",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # search_vector = SearchVectorField(editable=False, null=True)

    objects = ChallengeManager()

    # class Meta:
    # indexes = [GinIndex(fields=["search_vector"])]

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    @property
    def is_failed(self):
        return self.status == self.Status.FAILED

    def calculate_xp_bonus(self):
        xp_bonus = 0
        if self.due_date and self.due_date > timezone.now():
            xp_bonus += round(
                (self.difficulty.xp_value / 100)
                * Challenge.XP_PERCENTAGE_BONUS_FOR_DUE_DATE
            )
        return xp_bonus

    def adjust_xp(self, status):
        xp_value = self.difficulty.xp_value
        if status == Challenge.Status.COMPLETED:
            xp_value += self.calculate_xp_bonus()
            self.user.add_xp(xp_value)
        elif status == Challenge.Status.FAILED:
            self.user.subtract_xp(xp_value)
