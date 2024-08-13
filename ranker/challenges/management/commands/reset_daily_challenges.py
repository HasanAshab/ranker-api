from django.core.management.base import (
    BaseCommand,
)
from ranker.challenges.models import Challenge


class Command(BaseCommand):
    help = "Reset daily challenges of all users"

    def handle(self, *args, **options):
        Challenge.objects.filter(
            repeat_type=Challenge.RepeatType.DAILY,
        ).exclude(status=Challenge.Status.ACTIVE).update(
            status=Challenge.Status.ACTIVE
        )

        daily_challenges = Challenge.objects.filter(
            repeat_type=Challenge.RepeatType.DAILY,
        )

        for challenge in daily_challenges:
            challenge.status = Challenge.Status.ACTIVE
            challenge.save()

        self.stdout.write("Successfully reset daily challenges of all users")
