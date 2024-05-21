from django.urls import path
from .views import (
    ProfileView,
    SuggestUsernameView,
    PhoneNumberView,
)


urlpatterns = [
    path(
        "account/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "account/phone-number/",
        PhoneNumberView.as_view(),
        name="phone-number",
    ),
    path(
        "account/suggest-username/",
        SuggestUsernameView.as_view(),
        name="suggest-username",
    ),
]
