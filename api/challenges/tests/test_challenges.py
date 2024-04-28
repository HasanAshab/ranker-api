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
from api.challenges.serializers import (
    ListChallengeSerializer,
    ChallengeSerializer,
)


class challengesTestCase(APITestCase):
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
        url = reverse("challenges")
        challenges = ChallengeFactory.create_batch(3)
        data = ListChallengeSerializer(challenges, many=True).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)

    def test_retrieve_challenge_needs_authentication(self):
        url = reverse("challenge", args=[1])
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_challenge(self):
        challenge = ChallengeFactory()
        data = ChallengeSerializer(challenge).data
        url = reverse("challenge", kwargs={"pk": challenge.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)
