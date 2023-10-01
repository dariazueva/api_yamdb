from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserRegistrationViewSet, TokenObtainView

router_version1 = DefaultRouter()



urlpatterns = [
    path('auth/signup/', UserRegistrationViewSet.as_view({'post':'create'}), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]