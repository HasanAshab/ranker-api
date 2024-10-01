from django.core.management.base import (
    BaseCommand,
)
from knox.models import get_token_model
from ranker.users.factories import (
    UserFactory,
)


AuthToken = get_token_model()


class Command(BaseCommand):
    help = "Create a user and obtain auth token for testing"

    def handle(self, *args, **options):
        user = UserFactory()
        _, token = AuthToken.objects.create(user)
        self.stdout.write("Email: " + user.email)
        self.stdout.write("Username: " + user.username)
        self.stdout.write("Password: " + UserFactory.plain_password)
        self.stdout.write(self.style.SUCCESS(f"Token: {token}"))
