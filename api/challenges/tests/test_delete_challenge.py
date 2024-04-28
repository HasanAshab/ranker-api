from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.challenges.models import Challenge
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
            "user-details",
            kwargs={"pk": challenge.pk},
        )
    
    def test_needs_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_challenge(self):
        challenge = ChallengeFactory(user=self.user)
        
        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, payload)
        challenge_deleted = not Challenge.objects.filter(user=self.user).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(challenge_deleted)

    def test_can_not_delete_incomplete_challenge(self):
        pass
    
    def test_can_not_delete_others_challenge(self):
        pass
