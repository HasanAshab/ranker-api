from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.challenges.factories import (
    ChallengeFactory,
)


@tag("challenges", "challenge_steps", "create_challenge_step")
class CreateChallengeStepTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        url = reverse("challenge_steps", args=[1])
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_challenge_step(self):
        challenge = ChallengeFactory(user=self.user)
        payload = {
            "title": "test",
            "challenge": challenge.pk,
        }

        url = reverse("challenge_steps", kwargs={"pk": challenge.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertIsNotNone(challenge.steps.first())
