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


class UserModel(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    username_validator = UnicodeUsernameValidator()

    first_name = None
    last_name = None
    name = models.CharField(
        _("Name"),
        max_length=255,
        null=True,
    )
    gender = models.CharField(max_length=1, choices=Gender)
    username = models.CharField(
        _("username"),
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
    phone_number = PhoneNumberField(_("Phone Number"), null=True)
    avatar = models.ImageField(
        _("Avatar"),
        upload_to="uploads/avatars/",
        max_length=100,
        null=True,
    )

    @property
    def is_email_verified(self) -> bool:
        return self.emailaddress_set.filter(
            primary=True, verified=True
        ).exists()

    class Meta:
        db_table = "users"


User = LazyProxy(get_user_model)
