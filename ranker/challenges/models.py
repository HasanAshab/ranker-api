from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)

# from django.contrib.postgres.indexes import GinIndex
# from django.contrib.postgres.search import SearchVector, SearchVectorField
from dirtyfields import DirtyFieldsMixin
from datetime_validators.validators import date_time_is_future_validator
from .querysets import ChallengeQuerySet


class Challenge(DirtyFieldsMixin, models.Model):
    XP_PERCENTAGE_BONUS_FOR_DUE_DATE = 15
    XP_PENALTY_PERCENTAGE_FOR_FAILURE = 10

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")

    class RepeatType(models.TextChoices):
        NONE = "N", _("One-time")
        DAILY = "D", _("Daily")
        WEEKLY = "W", _("Weekly")

    title = models.CharField(
        _("Title"),
        max_length=50,
        help_text=_("Title of the challenge."),
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status,
        default=Status.ACTIVE,
        help_text=_("Status of the challenge."),
    )

    repeat_type = models.CharField(
        _("Repeat type"),
        max_length=1,
        choices=RepeatType,
        default=RepeatType.NONE,
        help_text=_("Repeat type of the challenge."),
    )
    is_pinned = models.BooleanField(
        _("Is Pinned"),
        default=False,
        help_text=_("Whether the challenge is pinned."),
    )
    due_date = models.DateTimeField(
        _("Due Date"),
        null=True,
        blank=True,
        help_text=_("Due date of the challenge."),
        validators=[date_time_is_future_validator],
    )
    order = models.IntegerField(
        _("Order"),
        default=1,
        help_text=_("Priority order of the challenge."),
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

    objects = ChallengeQuerySet.as_manager()

    # class Meta:
    # indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    @property
    def is_failed(self):
        return self.status == self.Status.FAILED

    def calculate_xp_reward(self):
        xp_bonus = self.difficulty.xp_value
        if self.due_date and self.due_date > timezone.now():
            xp_bonus += round(
                (self.difficulty.xp_value / 100)
                * Challenge.XP_PERCENTAGE_BONUS_FOR_DUE_DATE
            )
        return xp_bonus

    def calculate_failure_xp_penalty(self):
        xp_value = self.difficulty.xp_value
        return round(xp_value * (self.XP_PENALTY_PERCENTAGE_FOR_FAILURE / 100))

    def award_completion_xp(self):
        xp_reward = self.calculate_xp_reward()
        self.user.add_xp(xp_reward)

    def penalize_failure_xp(self):
        xp_penalty = self.calculate_failure_xp_penalty()
        self.user.subtract_xp(xp_penalty)


class ChallengeStep(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
        help_text=_("Title of the step."),
    )
    is_completed = models.BooleanField(
        _("Completed"),
        default=False,
        help_text=_("Whether the step is completed."),
    )
    order = models.IntegerField(
        _("Order"),
        default=1,
        help_text=_("Priority order of the step."),
    )
    challenge = models.ForeignKey(
        "challenges.Challenge",
        related_name="steps",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order", "id")


@receiver(
    models.signals.pre_save,
    sender=Challenge,
    dispatch_uid="set_order_of_pinned_challenge",
)
def set_order_of_pinned_challenge(sender, instance, **kwargs):
    if instance.is_pinned:
        instance.order = 0


@receiver(
    models.signals.post_save,
    sender=Challenge,
    dispatch_uid="update_user_xp_on_status_change",
)
def update_user_xp_on_status_change(sender, instance, created, **kwargs):
    if not created and "status" in instance.get_dirty_fields():
        if instance.status == Challenge.Status.COMPLETED:
            instance.award_completion_xp()
            instance.steps.all().delete()

        elif instance.status == Challenge.Status.FAILED:
            instance.penalize_failure_xp()
