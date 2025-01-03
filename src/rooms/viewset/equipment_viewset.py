from rest_framework import viewsets
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



    def destroy(self, request, *args, **kwargs):
        equipment = self.get_object()

        equipment.status = False
        equipment.save()

        return Response(
            {"message": f"L'équipement {equipment.id}-{equipment.name} a été désactivé avec succès."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        if self.action == 'reactivate':
            return EquipementModels.objects.all()
        return EquipementModels.objects.filter(status=True)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        equipment = self.get_object()
        equipment.status = True
        equipment.save()
        return Response(
            {"message": f"L'équipement {equipment.id}-{equipment.name} a été réactivé avec succès."},
            status=status.HTTP_200_OK
        )