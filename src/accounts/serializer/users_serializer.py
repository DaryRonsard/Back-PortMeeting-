from rest_framework import serializers
from accounts.models.user_models import UsersModels


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    avatar = serializers.ImageField(required=False, allow_null=True)  # Champ pour l'avatar

    class Meta:
        model = UsersModels
        fields = ['id', 'username', 'password', 'email', 'role', 'direction', 'avatar']

    def create(self, validated_data):
        # Extraire le mot de passe
        password = validated_data.pop('password')

        # Créer l'utilisateur
        user = UsersModels(**validated_data)
        user.set_password(password)  # Hash du mot de passe
        user.save()
        return user