from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .utils import generate_name_from_username


@receiver(user_signed_up, dispatch_uid="generate_name")
def generate_name(sender, request, user, **kwargs):
    user.name = generate_name_from_username(user.username)
    user.save()
