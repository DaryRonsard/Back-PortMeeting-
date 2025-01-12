from cloudinary.models import CloudinaryField
from django.db import models
from base.models.helpers.date_time_model import DateTimeModel
from rooms.models.room_models import RoomsModels


class PictureRoomModels(DateTimeModel):
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE, related_name='picture')
    image = CloudinaryField('images', blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Image de {self.salle.name} - {self.id}"