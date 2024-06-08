from django.conf import settings
from django.dispatch import receiver
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
        help_text=_("The title of the level"),
    )
    required_level = models.PositiveIntegerField(
        _("Required Level"),
        unique=True,
        help_text=_("Minimum level requirement to achieve the title"),
    )
    light_color = ColorField(
        _("Ligth Color"), help_text=_("The display color for ligth theme.")
    )
    dark_color = ColorField(
        _("Dark Color"), help_text=_("The display color for dark theme.")
    )

    objects = LevelTitleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-required_level",)


@receiver(
    models.signals.pre_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="set_level_title",
)
def set_level_title(sender, instance, **kwargs):
    if not instance.level_title:
        level_title = LevelTitle.objects.filter(
            required_level__lte=instance.level
        )
        instance.level_title = level_title
        instance.level_title = LevelTitle.objects.get_for_user(instance)


@receiver(
    models.signals.pre_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="update_level_title",
)
def update_level_title(sender, instance, **kwargs):
    if instance.has_leveled_up():
        level_title = LevelTitle.objects.filter(
            required_level=instance.level,
        ).first()
        if level_title:
            instance.level_title = level_title

    if (
        instance.has_leveled_down()
        and instance.level < instance.level_title.required_level
    ):
        level_title = LevelTitle.objects.filter(
            required_level__lte=instance.level
        ).first()
        instance.level_title = level_title


@receiver(
    models.signals.post_delete,
    sender=LevelTitle,
    dispatch_uid="demote_level_title",
)
def demote_level_title(sender, instance, **kwargs):
    level_title = LevelTitle.objects.get_previous(instance)
    instance.users.update(level_title=level_title)
