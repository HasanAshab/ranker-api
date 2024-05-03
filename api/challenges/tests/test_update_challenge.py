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


class UpdateChallengeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def _reverse_challenge_url(self, challenge):
        return reverse(
            "challenge",
            kwargs={"pk": challenge.pk},
        )

    def test_needs_authentication(self):
        url = reverse("challenge", args=[1])
        response = self.client.patch(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_update_challenge(self):
        data = {
            "title": "Updated Title",
            "description": "Updated Description",
        }
        challenge = ChallengeFactory(user=self.user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.title, data["title"])
        self.assertEqual(challenge.description, data["description"])

    def test_can_not_update_completed_challenge(self):
        challenge = ChallengeFactory(user=self.user, completed=True)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_update_failed_challenge(self):
        challenge = ChallengeFactory(user=self.user, failed=True)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_update_others_challenge(self):
        other_user = UserFactory()
        challenge = ChallengeFactory(user=other_user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
