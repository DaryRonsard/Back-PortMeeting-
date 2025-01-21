from rest_framework import serializers

from accounts.serializer.direction_serializer import DirectionSerializer
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.picture_rooms_serializer import PictureRoomSerializer


class RoomsSerializer(serializers.ModelSerializer):
    images = PictureRoomSerializer(many=True, read_only=True, source='picture')
    room_equipments = serializers.SerializerMethodField()
    direction_details = DirectionSerializer(source='direction', read_only=True)

    class Meta:
        model = RoomsModels
        fields = (
            'id', 'name', 'direction', 'capacite',
            'localisation', 'images', 'room_equipments',
            'direction_details'
        )

    def get_room_equipments(self, obj):
        from rooms.serializer.rooms_equipment_serializer import RoomEquipmentSerializer
        room_equipments = obj.room_equipments.all()
        if not room_equipments.exists():
            return []
        return RoomEquipmentSerializer(room_equipments, many=True).data

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
