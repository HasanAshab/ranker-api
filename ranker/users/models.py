from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth import (
    get_user_model,
)
from django.db import models
from django.contrib.auth.validators import (
    UnicodeUsernameValidator,
)
from django.utils.translation import (
    gettext_lazy as _,
)
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from dirtyfields import DirtyFieldsMixin
from ranker.common.utils import LazyProxy
from ranker.accounts.utils import generate_name_from_username
from .utils import calculate_level


class UserModel(DirtyFieldsMixin, AbstractUser):
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    username_validator = UnicodeUsernameValidator()

    level_title = models.ForeignKey(
        "level_titles.LevelTitle",
        on_delete=models.DO_NOTHING,
        related_name="users",
    )
    first_name = None
    last_name = None
    name = models.CharField(
        _("Name"), max_length=255, blank=True, help_text=_("Name of the user")
    )
    gender = models.CharField(
        _("Gender"),
        max_length=6,
        choices=Gender,
        default=Gender.MALE,
        help_text=_("Gender of the user"),
    )
    username = models.CharField(
        _("Username"),
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        help_text=_(
            f"Required. {settings.USERNAME_MAX_LENGTH} characters or fewer."
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone_number = PhoneNumberField(
        _("Phone Number"), blank=True, help_text=_("Phone number of the user")
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to="uploads/avatars/",
        max_length=100,
        blank=True,
        help_text=_("Avatar (or profile pic) of the user"),
    )
    rank = models.PositiveBigIntegerField(
        _("Rank"),
        help_text=_("Global rank of the user"),
    )
    total_xp = models.PositiveBigIntegerField(
        _("Total XP"), default=0, help_text=_("Total xp points of the user")
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        level_title = (
            self.level_title.title if self.level_title_id else "Unknown"
        )
        return f"{self.username} ({level_title})"

    @property
    def is_email_verified(self) -> bool:
        return self.emailaddress_set.filter(
            primary=True, verified=True
        ).exists()

    @property
    def level(self) -> int:
        return calculate_level(self.total_xp)

    @property
    def previous_level(self):
        previous_xp = self.get_dirty_fields().get("total_xp")
        if not previous_xp:
            return self.level
        return calculate_level(previous_xp)

    def add_xp(self, amount, commit=True):
        self.total_xp += amount
        if commit:
            self.save()

    def subtract_xp(self, amount, commit=True):
        if amount > self.total_xp:
            self.total_xp = 0
        else:
            self.total_xp -= amount
        if commit:
            self.save()


User: UserModel = LazyProxy(get_user_model)


@receiver(
    models.signals.pre_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="set_default_rank",
)
def set_default_rank(sender, instance, **kwargs):
    if instance._state.adding and not instance.rank:
        instance.rank = User.objects.count() + 1


@receiver(
    models.signals.pre_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="set_name",
)
def set_name(sender, instance, **kwargs):
    if instance._state.adding and not instance.name:
        instance.name = generate_name_from_username(instance.username)
