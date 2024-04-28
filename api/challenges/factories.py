import factory
from .models import Challenge


class ChallengeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence", nb_words=10)

    class Params:
        completed = factory.Trait(is_completed=True)
        pinned = factory.Trait(is_pinned=True)

    class Meta:
        model = Challenge
