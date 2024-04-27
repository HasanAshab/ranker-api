from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from django.utils.text import slugify
from colorfield.fields import ColorField


class Difficulty(models.Model):
    """
    A level of difficulty for a challenge.
    """
    def __str__(self):
        return self.name

    name = models.CharField(
        _("Name"),
        max_length=30,
        help_text="The display name of the difficulty level."
    )
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        max_length=30,
        help_text="The slugyfied version of the difficulty name."
    )
    color = ColorField(
        _("Color"),
        help_text="The display color of the difficulty level."
    )
    points = models.PositiveIntegerField(
        _("Points"),
        help_text="Number of points associated with this difficulty level."
    )

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
