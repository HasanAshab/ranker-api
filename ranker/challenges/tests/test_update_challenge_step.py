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


@tag("challenges", "challenge_steps", "update_challenge_step")
class UpdateChallengeStepTestCase(APITestCase):
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
        url = reverse("challenge_step", args=[1, 1])
        response = self.client.patch(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_update_challenge_step(self):
        title = "Updated Title"
        challenge = ChallengeFactory(user=self.user)
        challenge_step = ChallengeStepFactory(challenge=challenge)

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"title": title})
        challenge_step.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge_step.title, title)

    def test_completing_all_steps_completes_challenge(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step = ChallengeStepFactory(challenge=challenge)

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_completed": True})
        challenge.refresh_from_db()
        challenge_step.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(challenge_step.is_completed)
        self.assertTrue(challenge.is_completed)

    def foo(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step, _ = ChallengeStepFactory.create_batch(
            2, challenge=challenge
        )

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_completed": True})
        challenge.refresh_from_db()
        challenge_step.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(challenge_step.is_completed)
        self.assertFalse(challenge.is_completed)

    def test_can_not_update_others_challenge_step(self):
        challenge_step = ChallengeStepFactory()

        url = self._reverse_challenge_step_url(challenge_step)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
