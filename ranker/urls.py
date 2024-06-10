from django.urls import path, include


urlpatterns = [
    path(
        "api/",
        include("ranker.docs.urls"),
    ),
    path(
        "api/",
        include("ranker.authentication.urls"),
    ),
    path(
        "api/",
        include("ranker.accounts.urls"),
    ),
    path(
        "api/",
        include("ranker.users.urls"),
    ),
    path(
        "api/",
        include("ranker.recent_searches.urls"),
    ),
    path(
        "api/",
        include("ranker.level_titles.urls"),
    ),
    path(
        "api/",
        include("ranker.difficulties.urls"),
    ),
    path(
        "api/",
        include("ranker.challenges.urls"),
    ),
]
