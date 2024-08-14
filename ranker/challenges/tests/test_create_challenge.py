from datetime import timedelta
from django.test import tag
from django.urls import reverse
from django.utils import timezone
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
    fixtures = ["level_titles"]
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
            "due_date": timezone.now() + timedelta(days=1),
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(self.user.challenge_set.exists())

    def test_can_not_create_repeated_challenge_with_due_date(self):
        difficulty = DifficultyFactory()
        payload = {
            "title": "test",
            "difficulty": {"id": difficulty.pk},
            "repeat_type": Challenge.RepeatType.DAILY,
            "due_date": timezone.now() + timedelta(days=1),
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(self.user.challenge_set.exists())

    def test_can_create_repeat_once_challenge_with_due_date(self):
        difficulty = DifficultyFactory()
        payload = {
            "title": "test",
            "difficulty": {"id": difficulty.pk},
            "repeat_type": Challenge.RepeatType.ONCE,
            "due_date": timezone.now() + timedelta(days=1),
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(self.user.challenge_set.exists())
