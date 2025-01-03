from rest_framework import serializers
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels

class RoomsSerializer(serializers.ModelSerializer):
    equipment = serializers.PrimaryKeyRelatedField(
        queryset=EquipementModels.objects.all(), many=True, required=False
    )

    class Meta:
        model = RoomsModels
        fields = ('name', 'direction', 'capacite', 'image', 'localisation', 'equipment')

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment', [])  # Récupérer les équipements
        room = RoomsModels.objects.create(**validated_data)   # Créer la salle
        room.equipment.set(equipment_data)                    # Associer les équipements
        return room
