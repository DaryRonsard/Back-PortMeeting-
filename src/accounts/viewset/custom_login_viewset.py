from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.serializer.custom_login_serializer import CustomLoginSerializer


from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializer.custom_login_serializer import CustomLoginSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer



# class CustomLoginViewset(generics.GenericAPIView):
#     serializer_class = CustomLoginSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)