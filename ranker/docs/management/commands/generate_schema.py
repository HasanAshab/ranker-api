import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = (
        "Generates the OpenAPI schema and saves it to static/docs/schema.yml"
    )

    def handle(self, *args, **options):
        output_file = os.path.join(settings.SCHEMA_DIR, "schema.yml")

        if not os.path.exists(settings.SCHEMA_DIR):
            os.makedirs(settings.SCHEMA_DIR)

        self.stdout.write("Generating OpenAPI schema...")
        call_command("spectacular", "--file", output_file)
        self.stdout.write(f"Schema generated and saved to {output_file}")
