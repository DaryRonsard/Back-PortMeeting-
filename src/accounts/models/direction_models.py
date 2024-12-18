from django.db import models
from base.models.helpers.named_date_time_model import NamedDateTimeModel


class DirectionModels(NamedDateTimeModel):
    description = models.CharField(max_length=180)

    def __str__(self):
        return self.name