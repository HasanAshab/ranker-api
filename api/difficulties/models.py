from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from colorfield.fields import ColorField


class Difficulty(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=30,
        help_text="The display name of the difficulty level.",
    )
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        max_length=30,
        help_text="The slugyfied version of the difficulty name.",
    )
    light_color = ColorField(
        _("Ligth Color"), help_text="The display color for ligth theme."
    )
    dark_color = ColorField(
        _("Dark Color"), help_text="The display color for dark theme."
    )
    xp_value = models.PositiveIntegerField(
        _("XP Value"),
        help_text="Number of xp value associated with this difficulty level.",
    )

    class Meta:
        ordering = ("xp_value",)

    def __str__(self):
        return self.slug
