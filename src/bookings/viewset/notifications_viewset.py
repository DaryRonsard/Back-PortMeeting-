from bookings.models.notification_models import NotificationModels
from bookings.serializer.booking_serializer import BookingRoomSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class NotificationsViewSet(ModelViewSet):
    queryset = NotificationModels.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = [IsAuthenticated]




