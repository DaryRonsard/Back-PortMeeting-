from rest_framework import serializers
from bookings.models.plage_horaire_models import PlageHoraireModels
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class PlageHoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlageHoraireModels
        fields = ['id', 'salle', 'heure_debut', 'heure_fin']

    def validate(self, attrs):
        instance = PlageHoraireModels(**attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)
        return attrs
