from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.recent_searches.factories import (
    RecentUserSearchFactory,
)


@tag("recent_user_searches", "delete_recent_user_search")
class DeleteRecentUserSearchTestCase(APITestCase):
    fixtures = ["level_titles"]

    def setUp(self):
        self.user = UserFactory()

    def _reverse_recent_user_search_url(self, recent_user_search):
        return reverse(
            "recent_search",
            kwargs={"pk": recent_user_search.pk},
        )

    def test_delete_recent_user_search_needs_authentication(self):
        url = reverse("recent_search", args=[1])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_recent_user_search(self):
        search = RecentUserSearchFactory(user=self.user)

        url = self._reverse_recent_user_search_url(search)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(self.user.searches.exists())

    def test_delete_all_recent_user_searches(self):
        RecentUserSearchFactory.create_batch(3, user=self.user)

        url = reverse("recent_searches")
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(self.user.searches.exists())
