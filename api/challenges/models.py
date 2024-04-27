from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from api.common.validators import date_time_is_future_validator


class Challenge(models.Model):
    def __str__(self):
        return self.title

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
