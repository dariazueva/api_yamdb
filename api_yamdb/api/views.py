from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filter import TitleFilter
from api.mixins import CategoryGenreMixin
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdmin
from api.serializers import (CategorySerializer, CommentSerializer,
                             CustomTokenObtainSerializer, CustomUserSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserRegistrationSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для регистрации пользователей."""

    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenObtainPairView):
    """Представление для получения пользовательских JWT-токенов."""

    serializer_class = CustomTokenObtainSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользовательскими данными."""

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
        if request.user.is_admin or request.user.is_moderator:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=CustomUser.USER)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CategoryGenreMixin):
    """ViewSet для управления категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """ViewSet для управления жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для управления произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для управления отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        author = self.request.user

        if isinstance(author, AnonymousUser):
            author.id = 0

        serializer.save(author=author, title=title)
