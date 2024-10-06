from django.core.management.base import BaseCommand
from ranker.common.utils import chunk_queryset
from ranker.users.models import User
from ranker.challenges.models import Challenge


class Command(BaseCommand):
    help = "Reset expired challenges of all users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, **options):
        expired_challenges = Challenge.objects.expired().select_related("user")
        chunk_size = options["chunk"]
        expired_ids = []
        user_updates = {}

        for challenge_chunk in chunk_queryset(expired_challenges, chunk_size):
            for challenge in challenge_chunk:
                user = challenge.user
                expired_ids.append(challenge.pk)
                if user.pk not in user_updates:
                    user_updates[user.pk] = user
                challenge.penalize_failure_xp(commit=False)

            User.objects.bulk_update(user_updates.values(), ["total_xp"])

        Challenge.objects.filter(pk__in=expired_ids).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully removed {len(expired_ids)} expired challenges"
            )
        )
