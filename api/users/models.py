import math
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
from allauth.account.signals import user_signed_up
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from api.common.utils import LazyProxy
from api.accounts.utils import generate_name_from_username


class UserModel(AbstractUser):
    REQUIRED_FIELDS = ("gender",)

    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    username_validator = UnicodeUsernameValidator()

    first_name = None
    last_name = None
    name = models.CharField(
        _("Name"), max_length=255, blank=True, help_text=_("Name of the user")
    )
    gender = models.CharField(
        _("Gender"),
        max_length=1,
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

    @property
    def is_email_verified(self) -> bool:
        return self.emailaddress_set.filter(
            primary=True, verified=True
        ).exists()

    @property
    def level(self) -> int:
        return 1 + math.floor(self.total_xp / 1000)

    def add_xp(self, amount):
        self.total_xp += amount
        self.save()

    def subtract_xp(self, amount):
        if self.total_xp >= amount:
            self.total_xp -= amount
            self.save()


User = LazyProxy(get_user_model)


@receiver(
    models.signals.pre_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="set_default_rank",
)
def set_default_rank(sender, instance, **kwargs):
    if instance._state.adding and not instance.rank:
        instance.rank = User.objects.count() + 1


@receiver(user_signed_up, dispatch_uid="generate_name")
def generate_name(sender, request, user, **kwargs):
    user.name = generate_name_from_username(user.username)
    user.save()
