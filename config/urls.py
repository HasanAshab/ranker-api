from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def handler404(request, exception=None):
    return JsonResponse(
        {"message": "Page not found"},
        status=404,
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ranker.urls")),
]


if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
