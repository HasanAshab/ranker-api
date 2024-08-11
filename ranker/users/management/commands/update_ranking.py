from django.core.management.base import BaseCommand
from ranker.users.utils import update_ranking


class Command(BaseCommand):
    help = "Update user ranking"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, *args, **kwargs):
        update_ranking(kwargs["chunk"])
        self.stdout.write(self.style.SUCCESS("Ranks updated successfully"))
