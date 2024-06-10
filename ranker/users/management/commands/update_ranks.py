from django.core.management.base import BaseCommand
from ranker.users.models import User
from django.db import transaction


class Command(BaseCommand):
    help = "Update user ranks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, *args, **kwargs):
        users = User.objects.all().order_by("-total_xp", "-date_joined")
        current_rank = 1
        for chunk in self.chunk_queryset(users, kwargs["chunk"]):
            for user in chunk:
                user.rank = current_rank
                current_rank += 1

            with transaction.atomic():
                User.objects.bulk_update(chunk, ["rank"])

        self.stdout.write(self.style.SUCCESS("Ranks updated successfully"))

    def chunk_queryset(self, queryset, chunk_size):
        start_index = 0
        while True:
            chunk = queryset[start_index : start_index + chunk_size]
            if not chunk:
                break
            yield chunk
            start_index += chunk_size
