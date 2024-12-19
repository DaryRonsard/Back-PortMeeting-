from django.urls import path, include
from rest_framework import routers


from accounts.viewset.user_viewset import UserViewSet
from accounts.viewset.direction_viewset import DirectionViewSet

from accounts.viewset.custom_login_viewset import CustomTokenObtainPairView


router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='users')
router.register(r'directions', DirectionViewSet, basename='directions')

urlpatterns = [
    path('', include(router.urls)),
    #path('generate_token/', CustomLoginViewset.as_view(), name='login-and-generate-token'),


]
