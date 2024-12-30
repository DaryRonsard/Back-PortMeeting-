from rest_framework import serializers
from rooms.models.equipment_models import EquipementModels


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipementModels
        fields = ('name', 'etat')

    def create(self, validated_data):
        return EquipementModels.objects.create(**validated_data)
