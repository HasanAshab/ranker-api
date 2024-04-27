from django.urls import path
from .views import ChallengesView, ChallengesActivityView, ChallengeView

urlpatterns = [
    path("challenges/", ChallengesView.as_view(), name="challenges"),
    path(
        "challenges/activity",
        ChallengesActivityView.as_view(),
        name="challenges-activity",
    ),
    path("challenges/<int:pk>/", ChallengeView.as_view(), name="challenge"),
]
