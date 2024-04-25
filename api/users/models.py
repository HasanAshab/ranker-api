from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth import (
    get_user_model,
)
from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from api.common.utils import LazyProxy


class UserModel(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(
        _("Name"),
        max_length=255,
        null=True,
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
