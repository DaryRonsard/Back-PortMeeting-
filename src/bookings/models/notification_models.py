from django.db import models
from base.models.helpers.date_time_model import DateTimeModel
from accounts.models.user_models import UsersModels


class NotificationModels(DateTimeModel):
    ETAT_CHOICES = [
        ('envoyee', 'Envoyée'),
        ('lue', 'Lue'),
    ]

    user = models.ForeignKey(UsersModels, on_delete=models.CASCADE)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='envoyee')

    def __str__(self):
        return f"Notification {self.id} pour {self.user.username}"