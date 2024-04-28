from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.challenges.models import Challenge
from api.users.factories import (
    UserFactory,
)
from api.difficulties.factories import (
    DifficultyFactory,
)


class CreateChallengeTestCase(APITestCase):
    url = reverse("challenges")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_challenge(self):
        difficulty = DifficultyFactory()
        payload = {
            "title": "test",
            "difficulty": difficulty.pk,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)
        challenge = Challenge.objects.get(user=self.user)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertIsNotNone(challenge)
        self.assertTrue(challenge.is_active)
