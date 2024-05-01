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
    def setUp(self):
        self.user = UserFactory()

    def test_list_difficulties_needs_authentication(self):
        url = reverse("difficulties")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_difficulties(self):
        url = reverse("difficulties")
        difficulties = DifficultyFactory.create_batch(3)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), len(difficulties))

    def test_retrieve_difficulty_needs_authentication(self):
        url = reverse("difficulty", args=[1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_difficulty(self):
        difficulty = DifficultyFactory()
        data = DifficultySerializer(difficulty).data
        url = reverse("difficulty", kwargs={"pk": difficulty.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)
