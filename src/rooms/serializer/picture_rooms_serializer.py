from rest_framework import serializers
from ..models.room_models import RoomsModels
from ..models.picture_rooms_models import PictureRoomModels


class PictureRoomSerializer(serializers.ModelSerializer):
    image_file_debug = serializers.SerializerMethodField()
    class Meta:
        model = PictureRoomModels
        fields = ['id', 'image','salle' ,'description', 'image_file_debug']

    def get_image_file_debug(self, obj):
        return str(obj.image) if obj.image else "Aucune image"

    def validate_image(self, value):

        if not value:
            raise serializers.ValidationError("L'image est obligatoire.")

        if hasattr(value, 'content_type'):
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("Seuls les fichiers d'image sont autorisés.")

        return value