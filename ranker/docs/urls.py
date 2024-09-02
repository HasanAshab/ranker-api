from django.conf import settings
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import SchemaView


urlpatterns = [
    path(
        "docs/ui/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "docs/ui/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += [
        path("docs/schema/", SpectacularAPIView.as_view(), name="schema")
    ]
else:
    urlpatterns += [
        path("docs/schema/", SchemaView.as_view(), name="schema"),
    ]
