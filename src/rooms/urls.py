from django.urls import path, include
from rest_framework import routers


from rooms.viewset.rooms_viewset import RoomsViewSet
from rooms.viewset.equipment_viewset import EquipmentViewSet
from rooms.viewset.picture_rooms_viewset import PictureRoomsViewset
#from rooms.viewset.equipment_viewset import

router = routers.DefaultRouter()
router.register(r'rooms', RoomsViewSet, basename='rooms')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'pictures', PictureRoomsViewset, basename='picture')


urlpatterns = [
    path('', include(router.urls)),
]