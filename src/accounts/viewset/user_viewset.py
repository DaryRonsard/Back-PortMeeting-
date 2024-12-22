from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response


from accounts.models.user_models import UsersModels
from accounts.serializer.users_serializer import UserSerializer


from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UsersModels.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            user_count = UsersModels.objects.count()
            if user_count == 0:
                return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):

        user_count = UsersModels.objects.count()

        if user_count == 0:

            data = request.data.copy()
            data['role'] = 'super_admin'
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Super Administrateur créé avec succès.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        if not request.user.is_authenticated or request.user.role != 'super_admin':
            return Response(
                {"detail": "Seuls les Super Administrateurs peuvent créer de nouveaux utilisateurs."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Utilisateur créé avec succès.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )




