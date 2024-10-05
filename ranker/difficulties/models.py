from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from colorfield.fields import ColorField


class Difficulty(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=30,
        help_text=_("The display name of the difficulty level."),
    )
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        max_length=30,
        help_text=_("The slugyfied version of the difficulty name."),
    )
    light_color = ColorField(
        _("Ligth Color"), help_text=_("The display color for ligth theme.")
    )
    dark_color = ColorField(
        _("Dark Color"), help_text=_("The display color for dark theme.")
    )
    xp_value = models.PositiveSmallIntegerField(
        _("XP Value"),
        help_text=_(
            "Number of xp value associated with this difficulty level."
        ),
    )
    xp_penalty = models.PositiveSmallIntegerField(
        _("XP Penalty"),
        help_text=_(
            "The amount of XP deducted when"
            "a challenge of this difficulty is failed."
        ),
    )

    class Meta:
        ordering = ("xp_value",)

    def __str__(self):
        return self.name
