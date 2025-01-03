from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from rooms.models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.rooms_serializer import RoomsSerializer
from rooms.models.room_models import RoomsModels
from rest_framework.viewsets import ModelViewSet

from rest_framework import status, viewsets


class RoomsViewSet(viewsets.ModelViewSet):
    serializer_class = RoomsSerializer
    queryset = RoomsModels.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, salle_id):
        try:
            salle = RoomsModels.objects.get(id=salle_id)
            equipements_ids = request.data.get('equipment', [])
            equipements = EquipementModels.objects.filter(id__in=equipements_ids)
            salle.equipements.add(*equipements)
            return Response({"message": "Équipements ajoutés avec succès"}, status=status.HTTP_200_OK)
        except RoomsModels.DoesNotExist:
            return Response({"error": "Salle non trouvée"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'])
    def add_equipment(self, request, pk=None):
        equipment = self.get_object()
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def create(self, request, *args, **kwargs):
        data = request.data
        equipment_ids = data.get('equipment', [])
        salle_serializer = self.get_serializer(data=data)
        if salle_serializer.is_valid():
            salle = salle_serializer.save()
            if equipment_ids:
                equipment = EquipementModels.objects.filter(id__in=equipment_ids)
                salle.equipment.add(*equipment)
            return Response(salle_serializer.data, status=status.HTTP_201_CREATED)
        return Response(salle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        rooms = self.get_object()

        rooms.status = False
        rooms.save()

        return Response(
            {"message": f"La salle {rooms.id}-{rooms.name} a été désactivé avec succès."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        if self.action == 'reactivate':
            return RoomsModels.objects.all()
        return RoomsModels.objects.filter(status=True)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        rooms = self.get_object()
        rooms.status = True
        rooms.save()
        return Response(
            {"message": f"La salle {rooms.id}-{rooms.name} a été réactivé avec succès."},
            status=status.HTTP_200_OK
        )
