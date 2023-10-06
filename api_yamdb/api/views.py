from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, status, viewsets, mixins, pagination
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsAdmin
from api.serializers import (CustomTokenObtainSerializer, CustomUserSerializer,
                             UserRegistrationSerializer)
from users.models import CustomUser

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from .filter import FilterByName, ExtendedFilter


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


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=('get', 'patch'),
            permission_classes=(IsAuthenticated,),
            serializer_class=CustomUserSerializer)
    def me(self, request):
        serializer = CustomUserSerializer(request.user,
                                          data=request.data,
                                          partial=True)
        if request.user.role == 'admin' or request.user.role == 'moderator':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(FilterByName, mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(FilterByName, mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'


class TitlesViewSet(ExtendedFilter, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
