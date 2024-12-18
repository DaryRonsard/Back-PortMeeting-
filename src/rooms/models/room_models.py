from django.db import models
from accounts.models.direction_models import DirectionModels
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class RoomsModels(NamedDateTimeModel):
    direction = models.ForeignKey(DirectionModels, on_delete=models.CASCADE)
    capacite = models.PositiveIntegerField()
    localisation = models.CharField(max_length=200)
    image = models.ImageField(upload_to='salles/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.direction.name}"