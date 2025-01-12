from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from accounts.models.direction_models import DirectionModels
from accounts.serializer.direction_serializer import DirectionSerializer
from bookings.models.booking_room_models import BookingRoomsModels
from bookings.serializer.booking_serializer import BookingRoomSerializer
from rooms.serializer.rooms_serializer import RoomsSerializer


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer
    queryset = DirectionModels.objects.all()

    def get_permissions(self):
        return [
            IsAuthenticated()
        ]

    @action(detail=True, methods=['get'], url_path='rooms')
    def get_rooms(self, request, pk=None):

        try:
            direction = self.get_object()
            rooms = direction.rooms.all()
            serializer = RoomsSerializer(rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DirectionModels.DoesNotExist:
            return Response(
                {"error": "Direction non trouvée."},
                status=status.HTTP_404_NOT_FOUND
            )
