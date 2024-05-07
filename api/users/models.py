import math
from django.conf import settings
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
from api.common.utils import LazyProxy


def get_default_rank():
    total_users = UserModel.objects.count()
    return total_users + 1


class UserModel(AbstractUser):
    REQUIRED_FIELDS = ("gender",)

    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    username_validator = UnicodeUsernameValidator()

    first_name = None
    last_name = None
    name = models.CharField(
        _("Name"), max_length=255, blank=True, help_text="Name of the user"
    )
    gender = models.CharField(
        _("Gender"),
        max_length=1,
        choices=Gender,
        help_text="Gender of the user",
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
        _("Phone Number"), blank=True, help_text="Phone number of the user"
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to="uploads/avatars/",
        max_length=100,
        blank=True,
        help_text="Avatar (or profile pic) of the user",
    )
    rank = models.PositiveBigIntegerField(
        _("Rank"),
        default=get_default_rank,
        help_text="Global rank of the user",
    )
    total_xp = models.PositiveBigIntegerField(
        _("Total XP"), default=0, help_text="Total xp points of the user"
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
