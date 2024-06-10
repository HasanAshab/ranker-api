from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from .models import Difficulty
from .serializers import DifficultySerializer


class DifficultiesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class DifficultyView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer
