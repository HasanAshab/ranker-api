from allauth.headless.tokens.sessions import (
    SessionTokenStrategy as BaseSessionTokenStrategy,
)
from knox.views import LoginView


class SessionTokenStrategy(BaseSessionTokenStrategy):
    def create_access_token(self, request):
        _, token = LoginView(request=request).create_token()
        return token
