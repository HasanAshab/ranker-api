from django.urls import path, include


urlpatterns = [
    path(
        "api/",
        include("api.docs.urls"),
    ),
    path(
        "api/",
        include("api.authentication.urls"),
    ),
    path(
        "api/",
        include("api.users.urls"),
    ),
]
