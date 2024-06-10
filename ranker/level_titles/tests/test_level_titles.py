from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.level_titles.factories import (
    LevelTitleFactory,
)


@tag("level_titles", "list_level_titles")
class LevelTitlesTestCase(APITestCase):
    url = reverse("level_titles")

    def test_list_level_titles_needs_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_level_titles(self):
        level_titles = LevelTitleFactory.create_batch(3)
        user = UserFactory(level_title=level_titles[0])

        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), len(level_titles))
