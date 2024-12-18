from rest_framework import serializers
from accounts.models.user_models import UsersModels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = UsersModels
        fields = ('password')
        extra_kwargs = {'password': {'write_only': True}}
