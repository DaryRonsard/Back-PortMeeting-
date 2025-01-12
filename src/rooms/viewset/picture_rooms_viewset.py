from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models.picture_rooms_models import RoomsModels
from ..models.picture_rooms_models import PictureRoomModels
from ..serializer.picture_rooms_serializer import PictureRoomSerializer



class PictureRoomsViewset(ModelViewSet):
    serializer_class = PictureRoomSerializer
    queryset = PictureRoomModels.objects.all()
    permission_classes = [IsAuthenticated]