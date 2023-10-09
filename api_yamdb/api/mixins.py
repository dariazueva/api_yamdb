from rest_framework import viewsets, filters
from .permissions import IsAdminOrReadOnly


class CategoryGenreMixin(viewsets.GenericViewSet,
                         viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.DestroyModelMixin,
                         viewsets.mixins.ListModelMixin,
                         ):
    """Миксин для вьюсетов Категории и Жанры"""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
