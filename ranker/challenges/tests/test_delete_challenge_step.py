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
    ChallengeStepFactory,
)


@tag("challenges", "challenge_steps", "delete_challenge_step")
class DeleteChallengeStepTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def _reverse_challenge_step_url(self, challenge_step):
        return reverse(
            "challenge_step",
            kwargs={
                "pk": challenge_step.challenge.pk,
                "step_pk": challenge_step.pk,
            },
        )

    def test_needs_authentication(self):
        url = reverse("challenge", args=[1])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_challenge_step(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step = ChallengeStepFactory(challenge=challenge)

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(challenge.steps.exists())

    def test_can_not_delete_others_challenge_step(self):
        challenge_step = ChallengeStepFactory()

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertTrue(challenge_step.challenge.steps.exists())
