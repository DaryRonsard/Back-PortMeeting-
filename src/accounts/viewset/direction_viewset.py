from rest_framework import viewsets
from accounts.models.direction_models import DirectionModels
from accounts.serializer.direction_serializer import DirectionSerializer


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer
    queryset = DirectionModels.objects.all()