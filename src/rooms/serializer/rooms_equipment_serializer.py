from rest_framework import serializers
from rooms.models.rooms_equipment_models import RoomEquipmentModels
from rooms.serializer.equipment_serializer import EquipmentSerializer


class RoomEquipmentSerializer(serializers.ModelSerializer):
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)


    def to_representation(self, instance):
        from rooms.serializer.rooms_serializer import RoomsSerializer
        representation = super().to_representation(instance)
        representation['room_details'] = {
            "id": instance.salle.id,
            "name": instance.salle.name,
            "capacite": instance.salle.capacite,
            "localisation": instance.salle.localisation
        }
        return representation

    class Meta:
        model = RoomEquipmentModels
        fields = ('id', 'equipment', 'equipment_details', 'status')



    def get_equipment_details(self, obj):
        return {
            "id": obj.equipment.id,
            "name": obj.equipment.name,
            "etat": obj.equipment.etat,
        }
