from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rooms.models.equipment_models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = EquipementModels.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_equipment(self, request, pk=None):
        equipment = self.get_object()
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        equipment = self.get_object()

        equipment.status = False
        equipment.save()

        return Response(
            {"message": f"L'équipement {equipment.id} a été désactivé avec succès."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        return EquipementModels.objects.filter(status=True)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        equipment = self.get_object()
        equipment.status = True
        equipment.save()
        return Response(
            {"message": f"L'équipement {equipment.id} a été réactivé avec succès."},
            status=status.HTTP_200_OK
        )