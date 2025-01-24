from ..models.booking_room_models import BookingRoomsModels
from rest_framework import serializers
from rooms.models.room_models import EquipementModels
from accounts.serializer.users_serializer import UserSerializer
from rooms.serializer.rooms_serializer import RoomsSerializer
from accounts.serializer.direction_serializer import DirectionSerializer

class BookingRoomSerializer(serializers.ModelSerializer):
    direction_details = DirectionSerializer(source='direction', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    salle_details = RoomsSerializer(source='salle', read_only=True)
    equipements_specifiques = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EquipementModels.objects.all(), required=False
    )
    class Meta:
        model = BookingRoomsModels
        fields = ('id', 'salle', 'user', 'date', 'heure_debut', 'heure_fin', 'equipements_specifiques', 'etat', 'status','user_details', 'salle_details', 'direction_details')

    def create(self, validated_data):
        equipements_specifiques = validated_data.pop('equipements_specifiques', [])
        booking = BookingRoomsModels.objects.create(**validated_data)


        booking.equipements_specifiques.set(equipements_specifiques)

        return booking

    def validate(self, data):
        salle = data['salle']
        date = data['date']
        heure_debut = data['heure_debut']
        heure_fin = data['heure_fin']

        reservation_id = self.instance.id if self.instance else None

        reservations_existantes = BookingRoomsModels.objects.filter(
            salle=salle,
            date=date,
            etat='validee'
        ).filter(
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut
        ).exclude(id=reservation_id)

        if reservations_existantes.exists():
            raise serializers.ValidationError(
                "La salle est déjà réservée pour la plage horaire demandée."
            )

        return data