import time
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from .utils import generate_login_token
from .serializers import TokenLoginSerializer


class LoginTokenSSEView(APIView):
    permission_classes = (IsAuthenticated,)

    def token_generator(self):
        while True:
            data = {
                "event": "message",
                "token": generate_login_token(self.request.user),
            }
            print(data)
            yield data
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
        api_token = serializer.save()
        return Response({"token": api_token})
