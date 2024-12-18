from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.user_models import UsersModels
from accounts.serializer.users_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UsersModels.objects.all()


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create_user(request):

        if request.user.role != 'super_admin':
            return Response({"detail": "Seuls les super administrateurs peuvent créer des utilisateurs."},
                            status=status.HTTP_403_FORBIDDEN)

        # Traiter la requête si c'est un super administrateur
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)