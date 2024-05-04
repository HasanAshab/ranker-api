from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.factories import (
    UserFactory,
)
from api.level_titles.factories import (
    LevelTitleFactory,
)


@tag("level_titles")
class LevelTitlesTestCase(APITestCase):
    url = reverse("level_titles")

    def setUp(self):
        self.user = UserFactory()

    def test_list_level_titles_needs_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_level_titles(self):
        level_titles = LevelTitleFactory.create_batch(3)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), len(level_titles))
