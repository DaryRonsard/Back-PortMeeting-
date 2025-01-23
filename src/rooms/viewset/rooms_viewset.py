from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from rooms.models import EquipementModels
from rooms.serializer.equipment_serializer import EquipmentSerializer
from rooms.serializer.rooms_serializer import RoomsSerializer
from rooms.models.rooms_equipment_models import RoomEquipmentModels
from rooms.serializer.rooms_equipment_serializer import RoomEquipmentSerializer
from rooms.models.room_models import RoomsModels
from rest_framework.viewsets import ModelViewSet

from rest_framework import status, viewsets


class RoomsViewSet(viewsets.ModelViewSet):
    serializer_class = RoomsSerializer
    queryset = RoomsModels.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='equipments')
    def get_equipments(self, request, pk=None):
        room = self.get_object()
        room_equipments = RoomEquipmentModels.objects.filter(salle=room)
        serializer = RoomEquipmentSerializer(room_equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=True, methods=['post'], url_path='add-equipment')
    def add_equipment(self, request, pk=None):
        room = self.get_object()
        equipment_ids = request.data.get('equipements', [])

        if not isinstance(equipment_ids, list) or not equipment_ids:
            return Response(
                {"error": "Une liste valide d'ID d'équipements est requise."},
                status=status.HTTP_400_BAD_REQUEST
            )


        equipment_queryset = EquipementModels.objects.filter(id__in=equipment_ids)
        valid_equipment_ids = {eq.id for eq in equipment_queryset}
        invalid_ids = set(equipment_ids) - valid_equipment_ids

        if invalid_ids:
            return Response(
                {"error": f"Les équipements suivants sont introuvables : {list(invalid_ids)}."},
                status=status.HTTP_404_NOT_FOUND
            )


        existing_associations = RoomEquipmentModels.objects.filter(
            salle=room, equipment_id__in=valid_equipment_ids
        ).values_list('equipment_id', flat=True)

        already_associated = list(existing_associations)
        new_associations = valid_equipment_ids - set(already_associated)


        for equipment_id in new_associations:
            equipment = EquipementModels.objects.get(id=equipment_id)
            RoomEquipmentModels.objects.create(salle=room, equipment=equipment)


        response = {
            "message": f"Équipements ajoutés avec succès à la salle '{room.name}'.",
            "déjà_associés": already_associated,
            "nouvellement_ajoutés": list(new_associations)
        }
        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_equipment(self, request, pk=None):
        room = self.get_object()
        equipment_id = request.data.get('equipment_id')
        if not equipment_id:
            return Response({"error": "ID de l'équipement requis."}, status=status.HTTP_400_BAD_REQUEST)

        room_equipment = RoomEquipmentModels.objects.filter(salle=room, equipment_id=equipment_id).first()
        if not room_equipment:
            return Response({"error": "Association équipement-salle non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        room_equipment.status = not room_equipment.status
        room_equipment.save()
        status_message = "activé" if room_equipment.status else "désactivé"
        return Response(
            {"message": f"L'équipement a été {status_message} pour cette salle."},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        equipment_ids = data.get('equipements', [])  # Récupérer les ID des équipements

        salle_serializer = self.get_serializer(data=data)
        if salle_serializer.is_valid():
            salle = salle_serializer.save()  # Le serializer gère la création des équipements et des images

            # Associer les équipements si des IDs ont été fournis
            if isinstance(equipment_ids, list) and equipment_ids:
                equipment_queryset = EquipementModels.objects.filter(id__in=equipment_ids)
                valid_equipment_ids = {eq.id for eq in equipment_queryset}
                invalid_ids = set(equipment_ids) - valid_equipment_ids

                if invalid_ids:
                    return Response(
                        {"error": f"Les équipements suivants sont introuvables : {list(invalid_ids)}."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                for equipment_id in valid_equipment_ids:
                    equipment = EquipementModels.objects.get(id=equipment_id)
                    RoomEquipmentModels.objects.create(salle=salle, equipment=equipment)

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


    @action(detail=True, methods=['get'], url_path='equipments')
    def get_equipments(self, request, pk=None):
        room = self.get_object()
        room_equipments = RoomEquipmentModels.objects.filter(salle=room)
        serializer = RoomEquipmentSerializer(room_equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)