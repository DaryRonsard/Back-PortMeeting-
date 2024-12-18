from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from base.models.helpers.date_time_model import DateTimeModel


class UsersModels(DateTimeModel, AbstractUser):
    ROLE_CHOICES = [
        ('employe', 'Employe'),
        ('secretaire', 'gestionnaire'),
        ('super_admin', 'Super Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    direction = models.ForeignKey('DirectionModels', on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=13)
    matricule = models.CharField(max_length=4)
    #avatar = CloudinaryField('avatar', blank=True, null=True)


    def __str__(self):
        return f"{self.username} - {self.role}"