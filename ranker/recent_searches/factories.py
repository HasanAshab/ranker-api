import factory
from .models import RecentUserSearch


class RecentUserSearchFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("api.users.factories.UserFactory")
    searched_user = factory.SubFactory("api.users.factories.UserFactory")

    class Meta:
        model = RecentUserSearch
