from django.http import StreamingHttpResponse
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView

# from .models import Difficulty
from .serializers import TokenLoginSerializer
import time


class TokenSSEView(APIView):
    permission_classes = (IsAuthenticated,)

    def token_generator(self):
        while True:
            token = 1
            yield token
            time.sleep(5)

    def get(self, request):
        return StreamingHttpResponse(
            self.token_generator(), content_type="text/event-stream"
        )


class TokenLoginView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenLoginSerializer

    def post(self, request):
        pass
