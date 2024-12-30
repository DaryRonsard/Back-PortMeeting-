from requests import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rooms.serializer.rooms_serializer import RoomsSerializer
from rooms.models.room_models import RoomsModels
from rest_framework.viewsets import ModelViewSet

from rest_framework import status, viewsets


class RoomsViewSet(viewsets.ModelViewSet):
    serializer_class = RoomsSerializer
    queryset = RoomsModels.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        rooms = self.get_object()

        rooms.status = False
        rooms.save()

        return Response(
            {"message": f"La salle {rooms.id}-{rooms.name} a été désactivé avec succès."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        if self.action == 'reactivate':
            return RoomsModels.objects.all()
        return RoomsModels.objects.filter(status=True)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        rooms = self.get_object()
        rooms.status = True
        rooms.save()
        return Response(
            {"message": f"La salle {rooms.id}-{rooms.name} a été réactivé avec succès."},
            status=status.HTTP_200_OK
        )
