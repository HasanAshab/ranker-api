import time
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from .utils import generate_login_token, login_using_token
from .serializers import LoginTokenSSESerializer, TokenLoginSerializer


class LoginTokenSSEView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginTokenSSESerializer

    def get(self, request):
        return StreamingHttpResponse(
            self._token_generator(), content_type="text/event-stream"
        )

    def _token_generator(self):
        while True:
            token = generate_login_token(self.request.user)
            yield self._get_response_data(token)
            time.sleep(settings.LOGIN_TOKEN_MAX_AGE)

    def _get_response_data(self, token):
        return {"success": True, "message": "OK", "data": {"token": token}}


class TokenLoginView(APIView):
    serializer_class = TokenLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        _, auth_token = login_using_token(token)
        return Response({"token": auth_token})
