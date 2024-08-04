from django.test import tag
from django.urls import reverse
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
    def test_token_login(self):
        url = reverse("token_login")
        user = UserFactory()
        token = generate_login_token(user)
        response = self.client.post(url, {"token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["token"])
        print(response.data)
