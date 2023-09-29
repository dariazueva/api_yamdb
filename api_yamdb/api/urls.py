from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserRegistrationViewSet, TokenObtainView

router_version1 = DefaultRouter()



urlpatterns = [
    path('auth/signup/', UserRegistrationViewSet, name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]