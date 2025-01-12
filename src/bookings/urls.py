from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .viewset.microsoft_consentement import obtenir_consentement
from .viewset.traite_consentement import consent_callback

from bookings.viewset.plage_horaire_viewset import PlageHoraireViewSet
from bookings.viewset.booking_viewset import BookingRoomViewSet

router = routers.DefaultRouter()

router.register(r'plage_horaire', PlageHoraireViewSet, basename='plage_horaire')
router.register(r'booking', BookingRoomViewSet, basename='booking')
urlpatterns = [
    path('', include(router.urls)),
    path('consent/', obtenir_consentement, name='obtenir_consentement'),
    path('consent_callback/', consent_callback, name='consent_callback'),
]
