from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.models import User
from ranker.users.factories import (
    UserFactory,
)


@tag("account", "profile")
class ProfileTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("profile")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_show_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], self.user.id)

    def test_update_profile(self):
        name = "New Name"
        username = "newusername"

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url, {"name": name, "username": username}
        )
        self.user.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.user.name, name)
        self.assertEqual(self.user.username, username)

    def test_delete_account(
        self,
    ):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        user_deleted = not User.objects.filter(pk=self.user.pk).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertTrue(user_deleted)
