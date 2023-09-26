from rest_framework import (viewsets, mixins,
                            pagination)

from compositions.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer)
from .filter import FilterByName, ExtendedFilter


class CategoryViewSet(FilterByName, mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination


class GenreViewSet(FilterByName, mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination


class TitlesViewSet(ExtendedFilter, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
