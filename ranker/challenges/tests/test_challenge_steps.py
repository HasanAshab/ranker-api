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


@tag("challenges", "challenge_steps", "list_challenge_steps")
class ChallengeStepsTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def test_list_challenge_steps_needs_authentication(self):
        url = reverse("challenge_steps", args=[1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_challenge_steps(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step = ChallengeStepFactory(challenge=challenge)

        url = reverse("challenge_steps", kwargs={"pk": challenge.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], challenge_step.id)

    def test_retrieve_challenge_step_needs_authentication(self):
        url = reverse("challenge_step", args=[1, 1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_challenge_step(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step = ChallengeStepFactory(challenge=challenge)

        url = reverse(
            "challenge_step",
            kwargs={"pk": challenge.pk, "step_pk": challenge_step.pk},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], challenge_step.id)
