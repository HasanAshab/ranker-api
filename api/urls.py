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
    path(
        "api/",
        include("api.recent_searches.urls"),
    ),
    path(
        "api/",
        include("api.level_titles.urls"),
    ),
    path(
        "api/",
        include("api.difficulties.urls"),
    ),
    path(
        "api/",
        include("api.challenges.urls"),
    ),
]
