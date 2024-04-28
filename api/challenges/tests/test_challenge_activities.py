from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.factories import (
    UserFactory,
)
from api.difficulties.factories import (
    DifficultyFactory,
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
        difficulty1, difficulty2 = DifficultyFactory.create_batch(2)
        ChallengeFactory.create_batch(2, user=self.user, failed=True)
        ChallengeFactory.create_batch(
            2, user=self.user, difficulty=difficulty1, completed=True
        )
        ChallengeFactory(
            user=self.user, difficulty=difficulty2, completed=True
        )
        expected_data = {
            "total": 5,
            "failed": 2,
            "completed": {
                "total": 3,
                "difficulties": [
                    {
                        "id": difficulty1.id,
                        "count": 2,
                    },
                    {
                        "id": difficulty2.id,
                        "count": 1,
                    },
                ],
            },
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
