# Generated by Django 5.1.3 on 2024-12-17 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRoomsModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=180)),
                ('date', models.DateField()),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validee'), ('rejete', 'Rejetee'), ('annulee', 'Annulee')], default='en_attente', max_length=20)),
                ('equipements_specifiques', models.ManyToManyField(blank=True, to='rooms.equipementmodels')),
                ('salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomsmodels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotificationModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('message', models.TextField()),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('etat', models.CharField(choices=[('envoyee', 'Envoyée'), ('lue', 'Lue')], default='envoyee', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
