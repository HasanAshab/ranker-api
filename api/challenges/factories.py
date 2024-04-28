import factory
from .models import Challenge


class ChallengeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Challenge

    class Params:
        completed = factory.Trait(status=Challenge.Status.COMPLETED)
        failed = factory.Trait(status=Challenge.Status.FAILED)
        pinned = factory.Trait(is_pinned=True)

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence", nb_words=10)
    difficulty = factory.SubFactory(
        "api.difficulties.factories.DifficultyFactory"
    )
    user = factory.SubFactory("api.users.factories.UserFactory")
