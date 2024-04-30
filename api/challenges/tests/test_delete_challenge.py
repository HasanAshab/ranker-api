from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.factories import (
    UserFactory,
)
from api.challenges.factories import (
    ChallengeFactory,
)


class DeleteChallengeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def _reverse_challenge_url(self, challenge):
        return reverse(
            "challenge",
            kwargs={"pk": challenge.pk},
        )

    def test_needs_authentication(self):
        url = reverse("challenge", args=[1])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_challenge(self):
        challenge = ChallengeFactory(user=self.user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(self.user.challenge_set.exists())

    def test_can_not_delete_completed_challenge(self):
        challenge = ChallengeFactory(user=self.user, completed=True)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_can_not_delete_failed_challenge(self):
        challenge = ChallengeFactory(user=self.user, failed=True)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_can_not_delete_others_challenge(self):
        other_user = UserFactory()
        challenge = ChallengeFactory(user=other_user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertTrue(other_user.challenge_set.exists())
