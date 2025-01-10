from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from bookings.models.plage_horaire_models import PlageHoraireModels
from bookings.serializer.plage_horaire_serializer import PlageHoraireSerializer


class PlageHoraireViewSet(viewsets.ModelViewSet):
    queryset = PlageHoraireModels.objects.all()
    serializer_class = PlageHoraireSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='salle/(?P<salle_id>[^/.]+)')
    def get_by_salle(self, request, salle_id=None):
        def get_by_salle(self, request, salle_id=None):
            """
            Récupère toutes les plages horaires associées à une salle spécifique.
            """
            plages_horaires = PlageHoraireModels.objects.filter(salle_id=salle_id)

            # Gérer le cas où aucune plage n'est trouvée
            if not plages_horaires.exists():
                return Response(
                    {"detail": "Aucune plage horaire trouvée pour cette salle."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PlageHoraireSerializer(plages_horaires, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = PlageHoraireSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
