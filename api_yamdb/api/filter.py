from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class FilterByName():
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)


class ExtendedFilter(FilterByName):
    filterset_fields = ('category', 'genre', 'year', 'name')
    search_fields = ('category', 'genre', 'year', 'name')
