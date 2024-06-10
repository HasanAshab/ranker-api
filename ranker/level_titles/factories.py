import factory
from .models import LevelTitle


class LevelTitleFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("name")
    required_level = factory.Sequence(lambda n: n)
    light_color = factory.Faker("hex_color")
    dark_color = factory.Faker("hex_color")

    class Meta:
        model = LevelTitle
