import factory
from .models import Challenge



class ChallengeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Challenge

    class Params:
        completed = factory.Trait(is_completed=True)
        pinned = factory.Trait(is_pinned=True)

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence", nb_words=10)
    difficulty = factory.SubFactory('api.difficulties.factories.DifficultyFactory')
    user = factory.SubFactory('api.users.factories.UserFactory')
