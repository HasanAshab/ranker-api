import factory
from .models import Difficulty


class DifficultyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.Faker("slug")
    light_color = factory.Faker("hex_color")
    dark_color = factory.Faker("hex_color")
    xp_value = factory.Faker("random_int", min=0, max=100)

    class Meta:
        model = Difficulty
