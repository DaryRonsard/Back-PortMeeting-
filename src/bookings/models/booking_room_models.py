from django.db import models
from accounts.models.user_models import UsersModels
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class BookingRoomsModels(NamedDateTimeModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validee'),
        ('rejete', 'Rejetee'),
        ('annulee', 'Annulee'),
    ]

    user = models.ForeignKey(UsersModels, on_delete=models.CASCADE)
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    equipements_specifiques = models.ManyToManyField(EquipementModels, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Réservation {self.id} - {self.salle.name} ({self.statut})"


