from rest_framework import serializers
from ..models.equipment_models import EquipementModels

class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        models : EquipementModels
        fields = '__all__'


    def create(self, validated_data):
        return EquipementModels.objects.create(**validated_data)