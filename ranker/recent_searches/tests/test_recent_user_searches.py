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


@tag("recent_user_searches", "list_recent_user_searches")
class RecentUserSearchesTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("recent_searches")

    def setUp(self):
        self.user = UserFactory()

    def test_list_recent_user_searches_needs_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_recent_user_searches(self):
        searches = RecentUserSearchFactory.create_batch(3, user=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data["results"]), len(searches))
