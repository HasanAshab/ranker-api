from django.urls import path
from .views import RecentUserSearchesView, RecentUserSearchView

urlpatterns = [
    path(
        "recent-searches/",
        RecentUserSearchesView.as_view(),
        name="recent_searches",
    ),
    path(
        "recent-searches/<int:pk>/",
        RecentUserSearchView.as_view(),
        name="recent_search",
    ),
]
