from django.db import models
from rooms.models.room_models import RoomsModels

class PlageHoraireModels(models.Model):
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.salle.name} : {self.heure_debut} - {self.heure_fin}"

    def save(self, *args, **kwargs):

        plages_existantes = PlageHoraireModels.objects.filter(
            salle=self.salle
        ).filter(
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        )

        if plages_existantes.exists():
            raise ValueError("Cette plage horaire chevauche une autre plage existante.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.salle.name} : {self.heure_debut} - {self.heure_fin}"