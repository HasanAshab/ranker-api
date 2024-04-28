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


class ChallengeActivitiesTestCase(APITestCase):
    url = reverse("challenge-activities")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_show_challenge_activities(self):
        challenge = ChallengeFactory(user=self.user, completed=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "id": challenge.difficulty.id,
                    "name": challenge.difficulty.name,
                    "count": 1,
                }
            ],
        )

    def test_challenge_activities_excludes_incomplete_challenges(self):
        ChallengeFactory(user=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_challenge_activities_exludes_others_challenges(self):
        other_user = UserFactory()
        ChallengeFactory(user=other_user, completed=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
