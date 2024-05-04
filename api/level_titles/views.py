from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import LevelTitle
from .serializers import ListLevelTitleSerializer


class LevelTitlesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LevelTitle.objects.all()
    serializer_class = ListLevelTitleSerializer
