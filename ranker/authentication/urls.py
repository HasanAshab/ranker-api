from django.urls import path, include
from .views import LoginTokenSSEView, TokenLoginView

urlpatterns = [
    path("_allauth/", include("allauth.headless.urls")),
    path("auth/token/sse/", LoginTokenSSEView.as_view(), name="token_sse"),
    path("auth/token/login/", TokenLoginView.as_view(), name="token_login"),
]
