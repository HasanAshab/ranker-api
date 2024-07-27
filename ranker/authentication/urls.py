from django.urls import path, include
from .views import TokenSSEView

urlpatterns = [
    path("_allauth/", include("allauth.headless.urls")),
    path("auth/token/sse/", TokenSSEView.as_view(), name="token_sse"),
    # path("auth/token/login")
]
