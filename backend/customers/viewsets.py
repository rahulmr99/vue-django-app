from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import *


class CustomersModelViewSet(ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersModelSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_fields = '__all__'
