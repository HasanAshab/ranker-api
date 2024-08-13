from django.test import tag
from django.urls import reverse

# from django.utils import timezone
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.difficulties.factories import (
    DifficultyFactory,
)
from ranker.challenges.models import Challenge


@tag("challenges", "create_challenge")
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
            "difficulty": {"id": difficulty.pk},
            "due_date": "",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertIsNotNone(self.user.challenge_set.first())

    def test_repeated_challenge_not_allow_due_date(self):
        difficulty = DifficultyFactory()
        payload = {
            "title": "test",
            "difficulty": {"id": difficulty.pk},
            "repeat_type": Challenge.RepeatModel.DAILY,
            "due_date": "",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertIsNotNone(self.user.challenge_set.first())
