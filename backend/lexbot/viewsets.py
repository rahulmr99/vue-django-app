from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from api_v1.pagination import StandardResultsSetPagination
from authentication_user.mixins import GetGenSettingsMixin
from . import models, serializers


class VoiceBotConfigViewset(GetGenSettingsMixin, ModelViewSet):
    queryset = models.VoiceBotConfig.objects.filter()
    serializer_class = serializers.VoiceBotConfigSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticated,)
