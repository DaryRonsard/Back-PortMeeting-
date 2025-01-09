from rest_framework import serializers
from bookings.models.plage_horaire_models import PlageHoraireModels

class PlageHoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlageHoraireModels
        fields = ['salle', 'heure_debut', 'heure_fin']


