from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_v1.pagination import StandardResultsSetPagination
from app_settings.mixins import DefaultFilterOptions
from authentication_user.models import Account
from authentication_user.mixins import GetGenSettingsMixin
from . import models, serializers
from authentication_user.choices import MAIL_STATUS


class WorkingPlanModelViewSet(DefaultFilterOptions, ModelViewSet):
    queryset = models.WorkingPlan.objects.filter()
    serializer_class = serializers.WorkingPlanModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def get_disable_dates(self, request):
        """in a week return the disabled days. like [0] for sunday """
        user_id = self.request.GET.get('users')
        available_days = self.queryset.filter(
            users_id=user_id, enable=True).values_list('day', flat=True)
        disabled_days = []
        for i in range(1, 8):
            if i not in available_days:
                disabled_days.append(
                    # 0 is sunday in bootstrap datepicker
                    # https://bootstrap-datepicker.readthedocs.io/en/latest/options.html#daysofweekdisabled
                    0 if i == 7 else i
                )
        return Response(disabled_days)

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def get_business_hours(self, request):
        serializer = serializers.BusinessHourSerializer(data=models.WorkingPlan.get_business_hours(request.user),
                                                        many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class BreaksModelViewSet(DefaultFilterOptions, ModelViewSet):
    queryset = models.Breaks.objects.all()
    serializer_class = serializers.BreaksModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)


class GeneralSettingsModelViewSet(ModelViewSet):
    queryset = models.GeneralSettings.objects.all()
    serializer_class = serializers.GeneralSettingsModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Reset the email subscribe status when company email changes
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_account = Account.objects.filter(
            generalsettings=instance, is_provider=True).first()
        user_account.email_subscription_status = MAIL_STATUS.subscribed.name
        user_account.save()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class InitialConfirmationModelViewSet(GetGenSettingsMixin, DefaultFilterOptions, ModelViewSet):
    queryset = models.InitialConfirmation.objects.filter()
    serializer_class = serializers.InitialConfirmationModelSerializer
    permission_classes = (IsAuthenticated,)


class CancellationSettingsModelViewSet(GetGenSettingsMixin, DefaultFilterOptions, ModelViewSet):
    queryset = models.CancellationSettings.objects.filter()
    serializer_class = serializers.CancellationSettingsModelSerializer
    permission_classes = (IsAuthenticated,)


class ReschedulingSettingsModelViewSet(GetGenSettingsMixin, DefaultFilterOptions, ModelViewSet):
    queryset = models.ReschedulingSettings.objects.filter()
    serializer_class = serializers.ReschedulingSettingsModelSerializer
    permission_classes = (IsAuthenticated,)


class ReminderModelViewSet(GetGenSettingsMixin, DefaultFilterOptions, ModelViewSet):
    queryset = models.Reminder.objects.all()
    serializer_class = serializers.ReminderModelSerializer
    permission_classes = (IsAuthenticated,)
