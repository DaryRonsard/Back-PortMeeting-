from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['role'] = user.role
        token['direction'] = str(user.direction) if hasattr(user, 'direction') else None
        token['email'] = user.email

        return token

# class CustomLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         # Authentification de l'utilisateur
#         user = authenticate(**data)
#         if not user:
#             raise ValidationError("Invalid credentials")
#
#         if not user.is_active:
#             raise ValidationError("This account is inactive.")
#
#         # Générer les tokens JWT pour l'utilisateur
#         refresh = RefreshToken.for_user(user)
#
#         # Sérialiser l'utilisateur
#         user_data = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'role': user.role,
#             'direction': user.direction,
#         }
#
#         # Retourner les tokens et l'utilisateur
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': user_data
#         }
