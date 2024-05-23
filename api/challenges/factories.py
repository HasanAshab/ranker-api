from datetime import timedelta
from django.utils import timezone
import factory
from .models import Challenge


class ChallengeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    difficulty = factory.SubFactory(
        "api.difficulties.factories.DifficultyFactory"
    )
    user = factory.SubFactory("api.users.factories.UserFactory")

    class Meta:
        model = Challenge

    class Params:
        completed = factory.Trait(status=Challenge.Status.COMPLETED)
        failed = factory.Trait(status=Challenge.Status.FAILED)
        pinned = factory.Trait(is_pinned=True)
        has_due_date = factory.Trait(
            due_date=timezone.now() + timedelta(days=1)
        )
