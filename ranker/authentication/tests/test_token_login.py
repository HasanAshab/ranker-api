from django.conf import settings
from django.test import tag
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)
from ranker.authentication.utils import generate_login_token


@tag("auth", "token_login")
class TokenLoginTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("token_login")

    def setUp(self):
        self.user = UserFactory()

    def test_login_using_valid_token(self):
        token = generate_login_token(self.user)
        response = self.client.post(self.url, {"token": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_using_invalid_token(self):
        response = self.client.post(self.url, {"token": "invalid_token"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_login_using_expired_token(self):
        token = generate_login_token(self.user)

        with freeze_time() as frozen_time:
            frozen_time.tick(delta=settings.LOGIN_TOKEN_MAX_AGE + 1)
            response = self.client.post(self.url, {"token": token})

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn("token", response.data)
