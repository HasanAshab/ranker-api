from unittest.mock import patch
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


@tag("challenges", "challenge_steps", "generate_challenge_steps")
class ChallengeStepsGenerationTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def test_challenge_steps_generation_needs_authentication(self):
        url = reverse("challenge_steps_generation", args=[1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("ranker.challenges.gpt.ChallengeStepsGPTCompletion.create")
    def test_generate_challenge_steps(self, mocked_challenge_steps_generator):
        mocked_challenge_steps_generator.return_value = ["test"]
        challenge = ChallengeFactory(user=self.user)

        url = reverse(
            "challenge_steps_generation", kwargs={"pk": challenge.pk}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertGreater(len(response.data), 0)
        self.assertTrue(challenge.steps.exists())
        mocked_challenge_steps_generator.assert_called_once()
