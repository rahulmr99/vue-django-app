from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication_user.mixins import GetGenSettingsMixin
from . import serializers, models


class ServiceModelViewSet(
    GetGenSettingsMixin,
    ModelViewSet,
):
    """users are not allowed to create new services. Only to update them."""
    queryset = models.Service.objects.filter()
    serializer_class = serializers.ServiceModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_fields = '__all__'

    @list_route(methods=['get'])
    def get_services(self, request):
        serializer = serializers.PublicServiceSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        provider_obj = serializer.validated_data.get('provider_obj', None)
        serializer = serializers.ServiceModelSerializer(provider_obj.services.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryModelViewSet(GetGenSettingsMixin, ModelViewSet):
    queryset = models.Category.objects.filter()
    serializer_class = serializers.CategoryModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = '__all__'
    filter_fields = '__all__'
