from rest_framework import serializers
from rooms.models.room_models import RoomsModels


class RoomsSerializer(serializers.ModelSerializer):
    class Meta :
        model = RoomsModels
        fields = ('name', 'direction', 'capacite', 'image', 'status', 'localisation')

    def create(self, validated_data):
        return RoomsModels.objects.create(**validated_data)