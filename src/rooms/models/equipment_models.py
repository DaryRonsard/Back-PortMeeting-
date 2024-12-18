from django.db import models
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class EquipementModels(NamedDateTimeModel):
    etat = models.CharField(max_length=50, choices=[
        ('disponible', 'Disponible'),
        ('en_maintenance', 'En maintenance'),
    ])

    def __str__(self):
        return self.name
