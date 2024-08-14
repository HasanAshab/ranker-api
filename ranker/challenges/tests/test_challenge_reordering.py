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


@tag("challenges", "challenge_reordering")
class ChallengeReorderingTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("challenge_orders")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.patch(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_reordering_challenge(self):
        challenge1 = ChallengeFactory(user=self.user)
        challenge2 = ChallengeFactory(user=self.user)
        challenge3 = ChallengeFactory(user=self.user)
        data = [
            {"id": challenge1.id, "order": 3},
            {"id": challenge2.id, "order": 2},
            {"id": challenge3.id, "order": 1},
        ]

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data)
        challenge1.refresh_from_db()
        challenge2.refresh_from_db()
        challenge3.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge1.order, 3)
        self.assertEqual(challenge2.order, 2)
        self.assertEqual(challenge3.order, 1)

    def test_can_not_reorder_pinned_challenge(self):
        challenge = ChallengeFactory(user=self.user)
        pinned_challenge = ChallengeFactory(user=self.user, pinned=True)
        data = [
            {"id": challenge.id, "order": 2},
            {"id": pinned_challenge.id, "order": 3},
        ]

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data)
        challenge.refresh_from_db()
        pinned_challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.order, 2)
        self.assertEqual(pinned_challenge.order, 0)
