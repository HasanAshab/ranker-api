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


@tag("challenges", "list_challenges")
class ChallengesTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def test_list_challenges_needs_authentication(self):
        url = reverse("challenges")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_challenges(self):
        challenge = ChallengeFactory(user=self.user)

        url = reverse("challenges")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        results = response.data["results"]
        difficulties_meta = response.data["meta"]["difficulties"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], challenge.id)
        self.assertEqual(len(difficulties_meta), 1)

    def test_not_list_completed_challenges(self):
        url = reverse("challenges")
        ChallengeFactory(user=self.user, completed=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        difficulties_meta = response.data["meta"]["difficulties"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data["results"]), 0)
        self.assertEqual(len(difficulties_meta), 0)

    def test_not_list_failed_challenges(self):
        url = reverse("challenges")
        ChallengeFactory(user=self.user, failed=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        difficulties_meta = response.data["meta"]["difficulties"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data["results"]), 0)
        self.assertEqual(len(difficulties_meta), 0)

    def test_retrieve_challenge_needs_authentication(self):
        url = reverse("challenge", args=[1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_challenge(self):
        challenge = ChallengeFactory(user=self.user)
        url = reverse("challenge", kwargs={"pk": challenge.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], challenge.id)

    def test_can_not_retrieve_completed_challenge(self):
        challenge = ChallengeFactory(user=self.user, completed=True)

        url = reverse("challenge", kwargs={"pk": challenge.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_can_not_retrieve_failed_challenge(self):
        challenge = ChallengeFactory(user=self.user, failed=True)

        url = reverse("challenge", kwargs={"pk": challenge.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
