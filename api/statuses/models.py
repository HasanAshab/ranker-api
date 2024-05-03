from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import (
    gettext_lazy as _,
)
from .managers import StatusManager


class Status(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        help_text="The display name of the status",
    )
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        max_length=50,
        help_text="The slugyfied version of the status name.",
    )
    required_level = models.IntegerField(
        _("Required Level"),
        help_text="Minimum level requirement to achieve the level",
    )
    light_color = ColorField(
        _("Ligth Color"), help_text="The display color for ligth theme."
    )
    dark_color = ColorField(
        _("Dark Color"), help_text="The display color for dark theme."
    )
    
    objects = StatusManager()

    def __str__(self):
        return self.slug
