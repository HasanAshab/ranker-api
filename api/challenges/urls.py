from django.urls import path
from .views import (
    ChallengesView,
    ChallengeActivitiesView,
    ChallengeView,
    ChallengeOrdersView,
    ChallengeStepsView,
    ChallengeStepOrdersView,
    ChallengeStepsGenerationView,
    ChallengeStepView,
)

urlpatterns = [
    path("challenges/", ChallengesView.as_view(), name="challenges"),
    path(
        "challenges/activities/",
        ChallengeActivitiesView.as_view(),
        name="challenge_activities",
    ),
    path(
        "challenges/order/",
        ChallengeOrdersView.as_view(),
        name="challenge_orders",
    ),
    path("challenges/<int:pk>/", ChallengeView.as_view(), name="challenge"),
    path(
        "challenges/<int:pk>/steps/",
        ChallengeStepsView.as_view(),
        name="challenge_steps",
    ),
    path(
        "challenges/<int:pk>/steps/order/",
        ChallengeStepOrdersView.as_view(),
        name="challenge_step_orders",
    ),
    path(
        "challenges/<int:pk>/steps/generation/",
        ChallengeStepsGenerationView.as_view(),
        name="challenge_steps_generation",
    ),
    path(
        "challenges/<int:pk>/steps/<int:step_pk>/",
        ChallengeStepView.as_view(),
        name="challenge_step",
    ),
]
