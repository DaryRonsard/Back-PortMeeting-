from rest_framework import serializers

from accounts.serializer.direction_serializer import DirectionSerializer
from rooms.models import PictureRoomModels
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.picture_rooms_serializer import PictureRoomSerializer


class RoomsSerializer(serializers.ModelSerializer):
    images = PictureRoomSerializer(many=True, read_only=True, source='picture')
    room_equipments = serializers.SerializerMethodField()
    direction_details = DirectionSerializer(source='direction', read_only=True)
    add_images = PictureRoomSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = RoomsModels
        fields = (
            'id', 'name', 'direction', 'capacite',
            'localisation', 'images', 'room_equipments',
            'direction_details', 'add_images'
        )

    def get_room_equipments(self, obj):
        from rooms.serializer.rooms_equipment_serializer import RoomEquipmentSerializer
        room_equipments = obj.room_equipments.all()
        if not room_equipments.exists():
            return []
        return RoomEquipmentSerializer(room_equipments, many=True).data

    def add(self, request, *args, **kwargs):
        print(f"Fichiers reçus : {request.FILES}")
        return super().create(request, *args, **kwargs)

    def create(self, validated_data):
        images_data = validated_data.pop('add_images', [])
        print(f"DEBUG: Images reçues dans validated_data: {images_data}")

        # Vérifier si validated_data contient les bons fichiers
        for image_data in images_data:
            print(f"DEBUG: Image_data complet : {image_data}")
            if 'image' not in image_data:
                print(f"DEBUG: Champ 'image' manquant dans {image_data}")
            if not image_data.get('image'):
                print(f"DEBUG: Champ 'image' vide ou invalide dans {image_data}")

        room = super().create(validated_data)
        for image_data in images_data:
            if 'image' in image_data and image_data['image']:
                PictureRoomModels.objects.create(salle=room, **image_data)
            else:
                print(f"Données d'image invalides ou incomplètes : {image_data}")

        return room

    # def get_images(self, obj):
    #     return [picture.image.url for picture in obj.picture.all() if picture.image]
