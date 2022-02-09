from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class DefaultFilterOptions(object):
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_fields = '__all__'
