from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def date_time_is_future_validator(value):
    message = _("Date must be in the future.")
    code = "date_is_future"
    if value < timezone.now():
        raise ValidationError(message, code=code)
