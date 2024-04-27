from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
]


def handler404(request, exception=None):
    return JsonResponse(
        {"message": "Page not found"},
        status=404,
    )
