import os
from cryptography.fernet import Fernet
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.conf import settings
from api.common.utils import env_file


class Command(BaseCommand):
    help = "Decrypt environment variables"

    def add_arguments(self, parser):
        parser.add_argument(
            "key",
            type=str,
            help="Encryption key (must be at least 16 chars)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite .env file if it already exists",
        )

    def handle(self, *args, **options):
        key = options["key"]
        force = options["force"]
        if len(key) < 16:
            raise CommandError('"key" must be at least 16 characters long')

        encrypted_env_file_path = settings.BASE_DIR / ".env.encrypted"
        if not os.path.exists(encrypted_env_file_path):
            raise CommandError(".env.encrypted file does not exist")

        with open(
            encrypted_env_file_path,
            "rb",
        ) as f:
            encrypted_env = f.read()

        cipher_suite = Fernet(key.encode())
        decrypted_env = cipher_suite.decrypt(encrypted_env)

        if not decrypted_env:
            raise CommandError("Invalid encryption key.")

        if os.path.exists(env_file.path) and not force:
            msg = ".env file already exists. \
            Do you want to overwrite it? (y/n): "
            overwrite = input(msg)
            if overwrite.lower() != "y":
                return self.stdout.write(decrypted_env)

        with env_file.open() as f:
            f.write(decrypted_env)
        msg = "Environment variables decrypted and saved to .env"
        self.stdout.write(self.style.SUCCESS(msg))
