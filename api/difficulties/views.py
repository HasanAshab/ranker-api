from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
)
from .models import Difficulty
from .serializers import ListDifficultySerializer


class DifficultiesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Difficulty.objects.all()
    serializer_class = ListDifficultySerializer
