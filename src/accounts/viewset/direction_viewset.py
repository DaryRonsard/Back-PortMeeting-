from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models.direction_models import DirectionModels
from accounts.serializer.direction_serializer import DirectionSerializer


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer
    queryset = DirectionModels.objects.all()

    # def get_permissions(self):
    #     return [
    #         IsAuthenticated()
    #     ]