from django.urls import path, include


urlpatterns = [path("_allauth/", include("allauth.headless.urls"))]
