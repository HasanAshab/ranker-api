from django.core.management.base import (
    BaseCommand,
)
from django.db import transaction
from ranker.common.utils import chunk_queryset
from ranker.users.models import User
from ranker.challenges.models import Challenge


class Command(BaseCommand):
    help = "Reset repeated challenges of all users"

    def add_arguments(self, parser):
        parser.add_argument(
            "repeat_type",
            type=str,
            choices=[
                Challenge.RepeatType.DAILY,
                Challenge.RepeatType.WEEKLY,
                Challenge.RepeatType.MONTHLY,
            ],
            help="Repeat type to be reset",
        )
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, repeat_type, **kwargs):
        self.seed()
        daily_challenges = (
            Challenge.objects.active()
            .repeated(repeat_type)
            .select_related("user")
        )
        for challenge_chunk in chunk_queryset(
            daily_challenges, kwargs["chunk"]
        ):
            user_chunk = set()
            for challenge in challenge_chunk:
                if challenge.user in user_chunk:
                    challenge.user = next(
                        (
                            user
                            for user in user_chunk
                            if user == challenge.user
                        ),
                        None,
                    )
                user_chunk.add(challenge.user)
                challenge.penalize_failure_xp(commit=False)
                challenge.mark_as_active(commit=False)

            with transaction.atomic():
                print(user_chunk)
                Challenge.objects.bulk_update(challenge_chunk, ["status"])
                User.objects.bulk_update(user_chunk, ["total_xp"])

        Challenge.objects.repeated(repeat_type).inactive().mark_as_active()
        self.stdout.write("Successfully reset daily challenges of all users")

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        print(self.user1, self.user1.total_xp)
        print(self.user2, self.user2.total_xp)

        print(self.user2.challenge_set.completed().count())

    def seed(self):
        from ranker.difficulties.models import Difficulty
        from ranker.users.factories import UserFactory
        from ranker.challenges.factories import ChallengeFactory

        Challenge.objects.all().delete()
        User.objects.all().delete()

        diff = Difficulty.objects.first()
        print(diff, diff.xp_value)

        self.user1 = UserFactory(username="hasan", total_xp=50)
        self.user2 = UserFactory(username="hossein", total_xp=100)

        ChallengeFactory(
            user=self.user2,
            repeat_type=Challenge.RepeatType.DAILY,
            difficulty=diff,
        )
        ChallengeFactory.create_batch(
            2,
            user=self.user1,
            repeat_type=Challenge.RepeatType.DAILY,
            difficulty=diff,
        )
        ChallengeFactory(
            user=self.user2,
            repeat_type=Challenge.RepeatType.DAILY,
            difficulty=diff,
            completed=True,
        )
