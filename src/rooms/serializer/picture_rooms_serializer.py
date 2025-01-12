from rest_framework import serializers
from ..models.room_models import RoomsModels
from ..models.picture_rooms_models import PictureRoomModels


class PictureRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureRoomModels
        fields = ['id', 'salle', 'image', 'description']