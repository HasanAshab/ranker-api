from django.core.management.base import (
    BaseCommand,
)
from knox.models import get_token_model
from ranker.users.models import User


AuthToken = get_token_model()


class Command(BaseCommand):
    help = "Obtain auth token of a user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, username, *args, **options):
        user = User.objects.get(username=username)
        _, token = AuthToken.objects.create(user)
        self.stdout.write(self.style.SUCCESS(f"Token: {token}"))
