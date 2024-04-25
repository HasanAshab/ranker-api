from django.core.management.base import (
    BaseCommand,
)
from api.users.factories import (
    UserFactory,
)
from knox.views import LoginView


class R:
    def __init__(self, user):
        self.user = user


class Command(BaseCommand):
    help = "Create a user and obtain auth token for testing"

    def handle(self, *args, **options):
        user = UserFactory()
        token = LoginView(request=R(user)).create_token()
        self.stdout.write("Email: " + user.email)
        self.stdout.write("Username: " + user.username)
        self.stdout.write("Password: " + UserFactory.plain_password)
        self.stdout.write(self.style.SUCCESS(f"Token: {token[1]}"))
