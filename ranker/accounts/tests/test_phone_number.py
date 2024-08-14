from django.test import tag
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from ranker.users.factories import (
    UserFactory,
)


@tag("account", "phone_number")
class PhoneNumberTestCase(APITestCase):
    fixtures = ["level_titles"]
    url = reverse("phone_number")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("ranker.common.utils.twilio_verification.send_through_sms")
    def test_update_phone_number_without_otp(self, mocked_verification_sender):
        phone_number = "+15005550006"

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"phone_number": phone_number},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
        )
        self.assertEqual(self.user.phone_number, "")
        mocked_verification_sender.assert_called_once_with(phone_number)

    @patch("ranker.common.utils.twilio_verification.is_valid")
    def test_update_phone_number_with_valid_otp(
        self, mocked_verification_checker
    ):
        mocked_verification_checker.return_value = True
        phone_number = "+15005550006"
        otp = "123456"

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"phone_number": phone_number, "otp": otp},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.user.phone_number, phone_number)
        mocked_verification_checker.assert_called_once_with(phone_number, otp)

    @patch("ranker.common.utils.twilio_verification.is_valid")
    def test_update_phone_number_with_invalid_otp(
        self, mocked_verification_checker
    ):
        mocked_verification_checker.return_value = False
        phone_number = "+15005550006"
        otp = "123456"

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"phone_number": phone_number, "otp": otp},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(self.user.phone_number, "")
        mocked_verification_checker.assert_called_once_with(phone_number, otp)

    def test_remove_phone_number(
        self,
    ):
        user = UserFactory(has_phone_number=True)

        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(user.phone_number, "")
