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


@tag("challenges", "challenge_steps", "challenge_step_reordering")
class ChallengeStepReorderingTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        url = reverse("challenge_step_orders", args=[1])
        response = self.client.patch(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_reordering_challenge_step(self):
        challenge = ChallengeFactory(user=self.user)
        challenge_step1, challenge_step2, challenge_step3 = (
            ChallengeStepFactory.create_batch(
                3,
                challenge=challenge,
            )
        )
        data = [
            {"id": challenge_step1.id, "order": 3},
            {"id": challenge_step2.id, "order": 2},
            {"id": challenge_step3.id, "order": 1},
        ]

        url = reverse("challenge_step_orders", kwargs={"pk": challenge.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        challenge_step1.refresh_from_db()
        challenge_step2.refresh_from_db()
        challenge_step3.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge_step1.order, 3)
        self.assertEqual(challenge_step2.order, 2)
        self.assertEqual(challenge_step3.order, 1)
