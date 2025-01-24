from django.db import models
from accounts.models.user_models import UsersModels
from rooms.models.room_models import RoomsModels
from rooms.models.equipment_models import EquipementModels
#from accounts.models.direction_models import DirectionModels
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class BookingRoomsModels(NamedDateTimeModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validee'),
        ('rejete', 'Rejetee'),
        ('annulee', 'Annulee'),
        ('libere', 'Libere'),
    ]

    user = models.ForeignKey(UsersModels, on_delete=models.CASCADE)
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE)
    #direction = models.ForeignKey(DirectionModels, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    equipements_specifiques = models.ManyToManyField(EquipementModels, blank=True)
    etat = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['salle', 'date', 'heure_debut', 'heure_fin'],
                name='unique_booking_constraint'
            )
        ]
        ordering = ['date', 'heure_debut']

    def save(self, *args, **kwargs):

        conflits = BookingRoomsModels.objects.filter(
            salle=self.salle,
            date=self.date,
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut,
            etat='validee'
        )
        if conflits.exists():
            raise ValueError("La salle est déjà réservée pour cette plage horaire.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Réservation {self.id} - Salle : {self.salle.name} - etat : {self.etat})"


