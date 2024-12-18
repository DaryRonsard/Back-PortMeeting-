from django.urls import path, include
from rest_framework import routers
from django.contrib import admin

from accounts.viewset.user_viewset import UserViewSet
from accounts.viewset.direction_viewset import DirectionViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='users')
router.register(r'directions', DirectionViewSet, basename='directions')

urlpatterns = [
    path('', include(router.urls)),

]
