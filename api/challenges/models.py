from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)


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
        help_text="Description of the challenge.",
        required=False,
    )
    is_pinned = models.CharField(
        _("Is Pinned"),
        max_length=30,
        help_text=" challenge.",
    )
    due_date = models.CharField(
        _("Due Date"),
        max_length=30,
        help_text="Title of the challenge.",
    )
    difficulty = models.B