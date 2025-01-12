from ..models.booking_room_models import BookingRoomsModels
from rest_framework import serializers
from rooms.models.room_models import EquipementModels


class BookingRoomSerializer(serializers.ModelSerializer):
    equipements_specifiques = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EquipementModels.objects.all(), required=False
    )
    class Meta:
        model = BookingRoomsModels
        fields = ('salle', 'user', 'date', 'heure_debut', 'heure_fin', 'equipements_specifiques', 'etat')

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


        reservations_existantes = BookingRoomsModels.objects.filter(
            salle=salle,
            date=date,
            etat='validee'
        ).filter(
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut
        )

        if reservations_existantes.exists():
            raise serializers.ValidationError(
                "La salle est déjà réservée pour la plage horaire demandée."
            )

        return data