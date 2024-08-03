import time
from django.conf import settings
from django.http import StreamingHttpResponse
from django.core.signing import TimestampSigner
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from knox.models import get_token_model
from ranker.users.models import User
from .serializers import TokenLoginSerializer


AuthToken = get_token_model()
login_token_signer = TimestampSigner(salt=settings.TOKEN_LOGIN_SALT)


class LoginTokenSSEView(APIView):
    permission_classes = (IsAuthenticated,)

    def token_generator(self):
        while True:
            token = login_token_signer.sign(self.request.user.username)
            yield token
            time.sleep(settings.TOKEN_LOGIN_MAX_AGE)

    def get(self, request):
        return StreamingHttpResponse(
            self.token_generator(), content_type="text/event-stream"
        )


class TokenLoginView(APIView):
    serializer_class = TokenLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = login_token_signer.unsign(
            serializer.data["token"], max_age=settings.TOKEN_LOGIN_MAX_AGE
        )
        user = User.objects.get(username=username)
        _, api_token = AuthToken.objects.create(user)
        return Response(api_token)
