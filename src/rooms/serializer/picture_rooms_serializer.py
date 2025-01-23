from rest_framework import serializers
from ..models.room_models import RoomsModels
from ..models.picture_rooms_models import PictureRoomModels


class PictureRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureRoomModels
        fields = ['id', 'image', 'description']

    def validate_image(self, value):
        """
        Vérifie que le champ image contient une valeur valide.
        """
        if not value:
            raise serializers.ValidationError("L'image est obligatoire.")

        # Optionnel : Ajouter des validations supplémentaires (par exemple, vérifier le type de fichier)
        if hasattr(value, 'content_type'):
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("Seuls les fichiers d'image sont autorisés.")

        return value