from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import (
    gettext_lazy as _,
)
from .managers import LevelTitleManager


class LevelTitle(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
        help_text="The title of the level",
    )
    required_level = models.PositiveIntegerField(
        _("Required Level"),
        unique=True,
        help_text="Minimum level requirement to achieve the title",
    )
    light_color = ColorField(
        _("Ligth Color"), help_text="The display color for ligth theme."
    )
    dark_color = ColorField(
        _("Dark Color"), help_text="The display color for dark theme."
    )

    objects = LevelTitleManager()

    def __str__(self):
        return self.title
