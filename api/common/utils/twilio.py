from django.conf import settings
from django_twilio.client import (
    twilio_client,
)


class TwilioVerificationService:
    def __init__(self, client, service_sid):
        self.client = client
        self.service = self.client.verify.services(service_sid)

    def send(self, phone, channel):
        return self.service.verifications.create(to=phone, channel=channel)

    def send_through_sms(self, phone):
        return self.send(phone, channel="sms")

    def send_through_call(self, phone):
        return self.send(phone, channel="call")

    def is_valid(self, phone, code):
        return self.service.verification_checks.create(to=phone, code=code)


twilio_verification = TwilioVerificationService(
    client=twilio_client,
    service_sid=settings.TWILIO_VERIFY_SERVICE_SID,
)
