from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from rooms.serializer.rooms_serializer import RoomsSerializer
from rooms.models.room_models import RoomsModels



class RoomsViewSet(CreateModelMixin, ListModelMixin):
    serializer_class = RoomsSerializer
    queryset = RoomsModels.objects.all()

    def get_permissions(self):
        return  [IsAuthenticated(), '''AllowAny(),''' ]

