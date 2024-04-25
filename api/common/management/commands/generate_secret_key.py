from django.core.management.base import (
    BaseCommand,
)
from django.core.management.utils import (
    get_random_secret_key,
)
from api.common.utils import env_file


class Command(BaseCommand):
    help = "Generates new Secret Key and store it to env file"

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        env_file.update(SECRET_KEY=secret_key)
        self.stdout.write(self.style.SUCCESS(f"Key: {secret_key}"))
