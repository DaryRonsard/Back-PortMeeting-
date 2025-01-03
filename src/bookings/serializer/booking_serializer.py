from ..models.booking_room_models import BookingRoomsModels
from rest_framework import serializers


class SerializerBooking(serializers.ModelSerializer):
    class Meta:
        models = BookingRoomsModels
        fields = ('id', 'salle', 'user', 'date', 'heure_debut', 'heure_fin', 'equipements_specifiques', 'statut')


        def create(self, validated_data):
            return BookingRoomsModels.objects.create(**validated_data)