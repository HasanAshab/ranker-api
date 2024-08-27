from django.test import tag
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from ranker.users.factories import UserFactory


@tag("auth", "login_token_sse")
class LoginTokenSSETestCase(APITestCase):
    url = reverse("login_token_sse")

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_needs_authentication(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("ranker.authentication.views.generate_login_token")
    @patch("time.sleep", return_value=None)  # Mock sleep to avoid delays
    def test_token_streaming(self, mock_sleep, mock_generate_login_token):
        mock_generate_login_token.return_value = "testtoken"

        response = self.client.get(self.url, stream=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/event-stream")
        content = b"".join(response.streaming_content).decode("utf-8")
        self.assertIn("testtoken", content)
