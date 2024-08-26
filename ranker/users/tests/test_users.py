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


@tag("users", "list_users")
class UsersTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def _reverse_user_url(self, user):
        return reverse(
            "user_details",
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

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], user2.id)

    def test_retrieving_user_with_source_search_creates_recent_search(
        self,
    ):
        user2 = UserFactory()

        url = self._reverse_user_url(user2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, {"source": "search"})
        search = self.user.searches.filter(searched_user=user2).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], user2.id)
        self.assertTrue(search)

    def test_retrieving_self_with_source_search_not_creates_recent_search(
        self,
    ):
        url = self._reverse_user_url(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, {"source": "search"})
        search = self.user.searches.filter(searched_user=self.user).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], self.user.id)
        self.assertFalse(search)

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
