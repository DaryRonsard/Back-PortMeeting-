from rest_framework import serializers
from rooms.models.rooms_equipment_models import RoomEquipmentModels
from rooms.models.equipment_models import EquipementModels


class RoomEquipmentSerializer(serializers.ModelSerializer):
    equipment_details = serializers.SerializerMethodField()

    class Meta:
        model = RoomEquipmentModels
        fields = ('id', 'equipment', 'equipment_details', 'status')

    def get_equipment_details(self, obj):
        return {
            "id": obj.equipment.id,
            "name": obj.equipment.name,
            "etat": obj.equipment.etat,
        }
