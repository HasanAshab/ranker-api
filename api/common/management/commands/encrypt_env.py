import string
import random
from django.core.management.base import (
    BaseCommand,
)
from django.conf import settings
from cryptography.fernet import Fernet
from api.common.utils import env_file


class Command(BaseCommand):
    help = "Encrypt environment variables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--key",
            type=str,
            default=self.generate_key(),
            help="Encryption key",
        )

    def generate_key(self):
        length = 16
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))

    def handle(self, *args, **options):
        key = options["key"]
        with env_file.open() as f:
            env_contents = f.read().encode()
        cipher_suite = Fernet(key.encode())
        encrypted_env = cipher_suite.encrypt(env_contents)
        encrypted_env_file_path = settings.BASE_DIR / ".env.encrypted"
        with open(
            encrypted_env_file_path,
            "wb",
        ) as f:
            f.write(encrypted_env)
        self.stdout.write(
            self.style.SUCCESS("Environment variables encrypted successfully.")
        )
        self.stdout.write(self.style.SUCCESS("Key: " + key))
