from django.core.management.base import BaseCommand
from django.db import transaction
from ranker.common.utils import chunk_queryset
from ranker.users.models import User


class Command(BaseCommand):
    help = "Update user ranking"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, *args, **options):
        users = User.objects.all().order_by("-total_xp", "-date_joined")
        current_rank = 1
        for chunk in chunk_queryset(users, options["chunk"]):
            for user in chunk:
                user.rank = current_rank
                current_rank += 1

            with transaction.atomic():
                User.objects.bulk_update(chunk, ["rank"])
        self.stdout.write(self.style.SUCCESS("Ranks updated successfully"))
