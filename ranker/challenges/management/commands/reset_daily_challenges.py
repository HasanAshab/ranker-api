from django.core.management.base import (
    BaseCommand,
)
from django.db import transaction
from ranker.common.utils import chunk_queryset
from ranker.users.models import User
from ranker.challenges.models import Challenge


class Command(BaseCommand):
    help = "Reset daily challenges of all users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, *args, **kwargs):
        # return self.seed()
        daily_challenges = Challenge.objects.daily().select_related("user")
        for challenge_chunk in chunk_queryset(
            daily_challenges, kwargs["chunk"]
        ):
            user_chunk = set()
            for challenge in challenge_chunk:
                user_chunk.add(challenge.user)
                challenge.penalize_failure_xp(commit=False)
                challenge.mark_as_active(commit=False)

            with transaction.atomic():
                Challenge.objects.bulk_update(challenge_chunk, ["status"])
                User.objects.bulk_update(user_chunk, ["total_xp"])

        Challenge.objects.daily().inactive().mark_as_active()
        self.stdout.write("Successfully reset daily challenges of all users")


"""
    def seed(self):
        from ranker.difficulties.models import Difficulty

        diff = Difficulty.objects.first()
        print(diff)
        # Clear existing data if needed (be careful in production)
        Challenge.objects.all().delete()
        User.objects.all().delete()

        # Create mock users
        users = [
            User(username=f"user{i}", total_xp=random.randint(0, 1000))
            for i in range(10)
        ]
        User.objects.bulk_create(users)

        challenge1 = Challenge.create(
            user=user, repeat_type=Challenge.RepeatType.DAILY, difficulty=diff
        )
        challenge1 = Challenge.create(
            user=user, repeat_type=Challenge.RepeatType.DAILY, difficulty=diff
        )
"""
