from django.urls import path
from .views import DifficultiesView

urlpatterns = [
    path("difficulties/", DifficultiesView.as_view(), name="difficulties"),
]
