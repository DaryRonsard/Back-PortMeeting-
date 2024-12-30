from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from rooms.serializer.rooms_serializer import RoomsSerializer
from rooms.models.room_models import RoomsModels

from rest_framework import status, viewsets


class RoomsViewSet(viewsets.ModelViewSet):
    serializer_class = RoomsSerializer
    queryset = RoomsModels.objects.all()

    # def get_permissions(self):
    #     return [IsAuthenticated(), '''AllowAny(),''']
