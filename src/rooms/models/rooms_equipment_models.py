from django.db import models
from accounts.models.direction_models import DirectionModels
from base.models.helpers.named_date_time_model import NamedDateTimeModel
from rooms.models.equipment_models import EquipementModels
from rooms.models.room_models import RoomsModels


class RoomEquipmentModels(NamedDateTimeModel):
    salle = models.ForeignKey(RoomsModels, on_delete=models.CASCADE, related_name='room_equipments')
    equipment = models.ForeignKey(EquipementModels, on_delete=models.CASCADE, related_name='room_equipments')

    def __str__(self):
        return f"Équipement {self.equipment.name} dans la salle {self.salle.name}"