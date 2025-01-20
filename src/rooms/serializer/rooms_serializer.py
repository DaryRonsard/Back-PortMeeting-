from cloudinary import logger
from rest_framework import serializers

from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.picture_rooms_serializer import PictureRoomSerializer
from rooms.models.picture_rooms_models import PictureRoomModels
from rooms.serializer.rooms_equipment_serializer import RoomEquipmentSerializer


class RoomsSerializer(serializers.ModelSerializer):
    #images = serializers.SerializerMethodField()
    room_equipments = RoomEquipmentSerializer(many=True, read_only=True)
    images = PictureRoomSerializer(many=True, read_only=True, source='picture')

    equipment = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EquipementModels.objects.all(), write_only=True
    )
    equipment_details = EquipmentSerializer(many=True, read_only=True, source='equipment')

    class Meta:
        model = RoomsModels
        fields = ('id', 'name', 'direction',
                  'capacite', 'localisation',
                  'images', 'equipment',
                  'equipment_details',
                  'room_equipments'
                  )

    def create(self, validated_data):
        #equipment_ids = validated_data.pop('equipment', [])
        #images_data = self.initial_data.get('images', [])
        room = super().create(validated_data)
        #room.equipment.add(*equipment_ids)
        # for image_data in images_data:
        #     try:
        #         PictureRoomModels.objects.create(
        #             salle=room,
        #             image=image_data.get('image'),
        #             description=image_data.get('description', '')
        #         )
        #     except Exception as e:
        #         logger.error(f"Erreur lors de l'ajout d'une image : {str(e)}")
        return room

    # def get_images(self, obj):
    #     return [picture.image.url for picture in obj.picture.all() if picture.image]
