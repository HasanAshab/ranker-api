from django.urls import path
from .views import DifficultiesView, DifficultyView

urlpatterns = [
    path("difficulties/", DifficultiesView.as_view(), name="difficulties"),
    path(
        "difficulties/<int:pk>/", DifficultyView.as_view(), name="difficulty"
    ),
]
