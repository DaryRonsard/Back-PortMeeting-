from rest_framework import serializers
from accounts.models.direction_models import DirectionModels


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionModels
        fields = ('description', 'name', 'images')

    def create(self, validated_data):
        return DirectionModels.objects.create(**validated_data)
