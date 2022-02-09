from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app_settings.models import FeedbackConfig
from . import models, serializers


class FeedbackConfigModelViewSet(ModelViewSet):
    queryset = FeedbackConfig.objects.filter()
    serializer_class = serializers.FeedbackConfigModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FeedbackConfig.objects.filter(generalsettings__account=self.request.user)


class CustomPaging(PageNumberPagination):
    page_size = 10


class FeedbackModelViewSet(ModelViewSet):
    queryset = models.Feedback.objects.filter()
    serializer_class = serializers.FeedbackModelSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaging

    def get_queryset(self):
        qs = super().get_queryset()

        # restrict to the company it is listing
        qs = qs.filter(calendardb__generalsettings_id=self.request.user.generalsettings_id)

        # upon listing only show feedback with less than 4 rating
        content = self.request.query_params.get('content')
        if content:
            qs = qs.filter(rating_given__lt=4)

        return qs.distinct()

    @list_route(methods=['get'])
    def reports(self, request):
        feedabacks = self.get_queryset()
        ratings = []
        total = feedabacks.count()

        for i in range(1, 6):
            count = feedabacks.filter(rating_given=i).count()
            rating_tot = round(((count / total) * 100), 2) if total else 0
            ratings.append({
                'name': i,
                'count': count,
                'percent': rating_tot,
            })

        return Response(ratings)
