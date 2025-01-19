from rest_framework import serializers
from accounts.models.user_models import UsersModels
from accounts.serializer.direction_serializer import DirectionSerializer


class UserSerializer(serializers.ModelSerializer):
    direction_details = DirectionSerializer(source='direction', read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UsersModels
        fields = ['username', 'password', 'email', 'role', 'matricule', 'direction_details', 'direction', 'avatar', 'phone_number']

    def create(self, validated_data):
        password = validated_data.pop('password')


        user = UsersModels(**validated_data)
        user.set_password(password)
        user.save()
        return user