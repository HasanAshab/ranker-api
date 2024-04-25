from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.models import User
from api.users.factories import (
    UserFactory,
)
from api.users.serializers import (
    UserDetailsSerializer,
)


class UsersTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def _reverse_user_url(self, user: User) -> str:
        return reverse(
            "user-details",
            kwargs={"username": user.username},
        )

    def test_list_users_needs_authentication(
        self,
    ):
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_users(self):
        url = reverse("users")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        results = response.data["results"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["id"],
            self.user.id,
        )

    def test_retrieving_user_needs_authentication(
        self,
    ):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_user(self):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)
        data = UserDetailsSerializer(user2).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)

    def test_deleting_user_needs_authentication(
        self,
    ):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_user(self):
        url = self._reverse_user_url(self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        user_deleted = not User.objects.filter(pk=self.user.pk).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertTrue(user_deleted)
