from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from colorfield.fields import ColorField
from .querysets import DifficultyQuerySet


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
    xp_value = models.PositiveIntegerField(
        _("XP Value"),
        validators=[
            MaxValueValidator(settings.XP_PER_LEVEL),
        ],
        help_text=_(
            "Number of xp value associated with this difficulty level."
        ),
    )

    objects = DifficultyQuerySet.as_manager()

    class Meta:
        ordering = ("xp_value",)

    def __str__(self):
        return self.name
