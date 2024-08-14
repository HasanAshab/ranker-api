from datetime import timedelta
from django.utils import timezone
import factory
from .models import Challenge, ChallengeStep


class ChallengeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    difficulty = factory.SubFactory(
        "ranker.difficulties.factories.DifficultyFactory"
    )
    user = factory.SubFactory("ranker.users.factories.UserFactory")

    class Meta:
        model = Challenge

    class Params:
        completed = factory.Trait(status=Challenge.Status.COMPLETED)
        failed = factory.Trait(status=Challenge.Status.FAILED)
        pinned = factory.Trait(is_pinned=True)
        has_due_date = factory.Trait(
            due_date=timezone.now() + timedelta(days=1)
        )
        repeated = factory.Trait(repeat_type=Challenge.RepeatType.DAILY)


class ChallengeStepFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    challenge = factory.SubFactory(
        "ranker.challenges.factories.ChallengeFactory"
    )

    class Meta:
        model = ChallengeStep
