from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from bookings.viewset.plage_horaire_viewset import PlageHoraireViewSet

router = routers.DefaultRouter()

router.register(r'plage_horaire', PlageHoraireViewSet, basename='plage_horaire')
#router.register(r'booking', PlageHoraireModels, basename='booking')
urlpatterns = [
    path('', include(router.urls)),
]
