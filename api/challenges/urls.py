from django.urls import path
from .views import (
    ChallengesView,
    ChallengeActivitiesView,
    ChallengeView,
    ChallengeOrdersView,
)

urlpatterns = [
    path("challenges/", ChallengesView.as_view(), name="challenges"),
    path(
        "challenges/activities",
        ChallengeActivitiesView.as_view(),
        name="challenge-activities",
    ),
    path(
        "challenges/order",
        ChallengeOrdersView.as_view(),
        name="challenge-orders",
    ),
    path("challenges/<int:pk>/", ChallengeView.as_view(), name="challenge"),
]
