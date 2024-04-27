from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.factories import (
    UserFactory,
)
from api.difficulties.factories import (
    DifficultyFactory,
)
from api.difficulties.serializers import (
    DifficultySerializer,
)


class DifficultiesTestCase(APITestCase):
    url = reverse("difficulties")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_difficulties(self):
        difficulties = DifficultyFactory.create_batch(3)
        data = DifficultySerializer(difficulties, many=True).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)
