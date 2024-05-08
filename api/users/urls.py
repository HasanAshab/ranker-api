from django.urls import path
from .views import (
    UsersView,
    ProfileView,
    UserDetailsView,
    SuggestUsernameView,
    PhoneNumberView,
)


urlpatterns = [
    path(
        "users/",
        UsersView.as_view(),
        name="users",
    ),
    path(
        "users/me/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "users/me/phone-number/",
        PhoneNumberView.as_view(),
        name="phone-number",
    ),
    path(
        "users/<str:username>/",
        UserDetailsView.as_view(),
        name="user-details",
    ),
    path(
        "users/suggest/username/",
        SuggestUsernameView.as_view(),
        name="suggest-username",
    ),
]
