from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.difficulties.factories import (
    DifficultyFactory,
)
from ranker.challenges.factories import (
    ChallengeFactory,
)


@tag("challenges", "challenge_activities")
class ChallengeActivitiesTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("challenge_activities")

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

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 5)
        self.assertEqual(response.data["failed"], 2)
        self.assertEqual(response.data["completed"]["total"], 3)
