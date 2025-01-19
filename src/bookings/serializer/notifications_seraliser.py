from rest_framework import serializers
from bookings.models.notification_models import NotificationModels
from bookings.serializer.booking_serializer import BookingRoomSerializer

class NotificationSerializer(serializers.ModelSerializer):
    room = BookingRoomSerializer(read_only=True, many=True,)
    class Meta:
        model = NotificationModels
        fields = ('id','message', 'date_envoi', 'etat')