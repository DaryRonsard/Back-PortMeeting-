from django.db import models
from rooms.models.room_models import RoomsModels
from django.core.exceptions import ValidationError
import re


class PlageHoraireModels(models.Model):
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE)
    heure_debut = models.CharField(max_length=5)
    heure_fin = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.salle.name} : {self.heure_debut} - {self.heure_fin}"

    def clean(self):
        # Vérification du format HH:MM
        time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"  # Regex pour le format HH:MM
        if not re.match(time_pattern, self.heure_debut):
            raise ValidationError("L'heure de début doit être au format HH:MM.")
        if not re.match(time_pattern, self.heure_fin):
            raise ValidationError("L'heure de fin doit être au format HH:MM.")


        if self.heure_debut >= self.heure_fin:
            raise ValidationError("L'heure de début doit être inférieure à l'heure de fin.")


        plages_existantes = PlageHoraireModels.objects.filter(
            salle=self.salle
        ).exclude(pk=self.pk).filter(
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        )

        if plages_existantes.exists():
            raise ValidationError("Cette plage horaire chevauche une autre plage existante.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)