from django.urls import path
from .views import LevelTitlesView

urlpatterns = [
    path("level-titles/", LevelTitlesView.as_view(), name="level_titles"),
]
