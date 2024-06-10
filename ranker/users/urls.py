from django.urls import path
from .views import (
    UsersView,
    UserDetailsView,
)


urlpatterns = [
    path(
        "users/",
        UsersView.as_view(),
        name="users",
    ),
    path(
        "users/<str:username>/",
        UserDetailsView.as_view(),
        name="user_details",
    ),
]
