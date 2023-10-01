from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import UserRegistrationSerializer, CustomTokenObtainSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Создание нового пользователя."""

    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer