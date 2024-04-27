import factory
from .models import Difficulty


class DifficultyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.Faker("slug")
    color = factory.Faker("hex_color")
    points = factory.Faker("random_int", min=0, max=100)

    class Meta:
        model = Difficulty
