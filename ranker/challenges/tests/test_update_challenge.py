from datetime import timedelta
from django.test import tag
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.challenges.models import Challenge
from ranker.challenges.factories import (
    ChallengeFactory,
    ChallengeStepFactory,
)


@tag("challenges", "update_challenge")
class UpdateChallengeTestCase(APITestCase):
    fixtures = ["level_titles"]

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
        title = "Updated Title"
        challenge = ChallengeFactory(user=self.user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"title": title})
        challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.title, title)

    def test_completing_challenge_also_completes_steps(self):
        challenge = ChallengeFactory(user=self.user)
        ChallengeStepFactory.create_batch(3, challenge=challenge)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, {"status": Challenge.Status.COMPLETED}
        )
        challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.COMPLETED)
        self.assertEqual(challenge.steps.all().completed().count(), 3)

    def test_completing_challenge_increase_xp(self):
        challenge = ChallengeFactory(user=self.user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, {"status": Challenge.Status.COMPLETED}
        )
        challenge.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.COMPLETED)
        self.assertEqual(self.user.total_xp, challenge.difficulty.xp_value)

    def test_completing_due_dated_challenge_increase_xp_with_bonus(self):
        challenge = ChallengeFactory(user=self.user, has_due_date=True)
        original_xp_value = challenge.difficulty.xp_value
        xp_value = round(
            original_xp_value
            + (
                (original_xp_value / 100)
                * Challenge.XP_PERCENTAGE_BONUS_FOR_DUE_DATE
            )
        )

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, {"status": Challenge.Status.COMPLETED}
        )
        challenge.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.COMPLETED)
        self.assertEqual(self.user.total_xp, xp_value)

    def test_completing_challenge_after_due_date_does_not_receive_bonus(self):
        challenge = ChallengeFactory(
            user=self.user, due_date=timezone.now() - timedelta(days=1)
        )

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            url, {"status": Challenge.Status.COMPLETED}
        )
        challenge.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.COMPLETED)
        self.assertEqual(self.user.total_xp, challenge.difficulty.xp_value)

    def test_failing_challenge_decrease_xp(self):
        challenge = ChallengeFactory(user=self.user)
        self.user.total_xp = challenge.calculate_failure_xp_penalty()

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"status": Challenge.Status.FAILED})
        challenge.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.FAILED)
        self.assertEqual(self.user.total_xp, 0)

    def test_failing_challenge_not_decrease_xp_when_total_xp_is_zero(self):
        challenge = ChallengeFactory(user=self.user)

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"status": Challenge.Status.FAILED})
        challenge.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(challenge.status, Challenge.Status.FAILED)
        self.assertEqual(self.user.total_xp, 0)

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
        challenge = ChallengeFactory()

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={"title": "New Title"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_update_repeated_challenge_with_due_date(self):
        data = {
            "due_date": timezone.now() + timedelta(days=1),
        }
        challenge = ChallengeFactory(user=self.user, repeated=True)
        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(challenge.due_date)

    def test_can_update_repeat_once_challenge_with_due_date(self):
        data = {
            "due_date": timezone.now() + timedelta(days=1),
        }
        challenge = ChallengeFactory(
            user=self.user, repeat_type=Challenge.RepeatType.ONCE
        )

        url = self._reverse_challenge_url(challenge)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        challenge.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(challenge.due_date)
