from django.test import tag
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


@tag("account", "suggest_username")
class SuggestUsernameViewTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("suggest_username")

    def test_suggest_username(self):
        data = {"prefix": "test", "max_suggestions": 3}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
