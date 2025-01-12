from cloudinary.models import CloudinaryField
from django.db import models
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class DirectionModels(NamedDateTimeModel):
    description = models.CharField(max_length=180)
    images = CloudinaryField('images', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Directions"

