from rest_framework import serializers
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.picture_rooms_serializer import PictureRoomSerializer

class RoomsSerializer(serializers.ModelSerializer):
    #images = serializers.SerializerMethodField()
    images = PictureRoomSerializer(many=True, read_only=True, source='picture')

    equipment = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EquipementModels.objects.all(), write_only=True
    )
    equipment_details = EquipmentSerializer(many=True, read_only=True, source='equipment')

    class Meta:
        model = RoomsModels
        fields = ('id', 'name', 'direction', 'capacite', 'localisation', 'images', 'equipment', 'equipment_details')

    def create(self, validated_data):
        equipment_ids = validated_data.pop('equipment', [])
        room = super().create(validated_data)
        room.equipment.add(*equipment_ids)
        return room

    # def get_images(self, obj):
    #     return [picture.image.url for picture in obj.picture.all() if picture.image]
