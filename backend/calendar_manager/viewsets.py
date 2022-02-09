import calendar
import datetime
import logging

import pytz
from django.db.models import Q
from django.http import HttpResponse
from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from lexbot.handlers import utils
from rest_framework import filters, status
import rest_framework.decorators
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_v1.pagination import StandardResultsSetPagination
from authentication_user.models import Account
from services.models import Service
from calendar_manager.filters import CalendarDbFilter
from calendar_manager.mixins import MassCalandarGenerator
from calendar_manager.models import CalendarDb
from calendar_manager.serializers import (
    CalendarDbModelSerializer, FreeDaySerializer, ResponseListSerializer, CancelSerializer, IcalOutlookSerializer,
    RecurringAddDateMassSerializer, RecurringResponseDateSerializer, FilterAppointmentSerializer,
    CalendarDbFullModelSerializer, GetDateAppointmentSerializer, CalendarDbMainFullModelSerializer,
    SaveCalendarAppointmentSerializer, )
from calendar_manager.utils import get_day_list, caption_maker, get_filtered_time_slots

logger = logging.getLogger(__file__)


class CalendarDbModelViewSet(ModelViewSet, MassCalandarGenerator, ):
    queryset = CalendarDb.objects.filter()
    serializer_class = CalendarDbModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ['book_datetime', 'start_datetime', ]
    filter_class = CalendarDbFilter
    search_fields = [
        # filter based on the provider
        'users_provider__name', 'users_provider__last_name', 'users_provider__username', 'users_provider__phone',
        'users_provider__mobile', 'users_provider__email',

        'users_customer__name', 'users_customer__last_name', 'users_customer__username', 'users_customer__phone',
        'users_customer__mobile', 'users_customer__email',
    ]

    @rest_framework.decorators.list_route(methods=['get'], permission_classes=[AllowAny])
    def checkin_booking_date(self, request):
        serializer = FreeDaySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get('page', 0)
        # service_id = serializer.validated_data.get('service_id', 0)
        provider_id = serializer.validated_data.get('provider_id', 0)
        user: Account = get_object_or_404(Account, id=provider_id)

        days_page = get_day_list(page, user=user)

        if serializer.validated_data.get('daydate'):
            date = (serializer.validated_data['daydate']).date()
            days = (date - datetime.date.today()).days
            tzname = user.timezone if user else 'US/Eastern'
            tzname = 'US/Eastern' if tzname == 'EST' else tzname
            tz_obj = pytz.timezone(tzname)
            timezone.activate(tz_obj)

            days_page: list = [timezone.now() + datetime.timedelta(days=days)]

        result = []

        # service = get_object_or_404(Service, id=service_id)

        for day_obj in days_page:
            day_name = day_obj.strftime('%A')
            breaks = user.breaks_set.filter()
            workingplan = user.workingplan_set.filter(
                day=day_obj.isoweekday()).first()

            # skip if particular date is not in the workingPlan
            if (not workingplan) or (not workingplan.enable):
                continue

            result.append({
                'name': day_name,
                'number': day_obj.strftime('%B %d'),
                'choice': False,
                'caption': caption_maker(day_obj),
                'date': get_filtered_time_slots(
                    day_obj, workingplan, user.appointment_interval, self.queryset, breaks, user=user)
            })

        serializer = ResponseListSerializer(
            data={'days': result}, context={'tzname': tzname})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @rest_framework.decorators.list_route(methods=['post'])
    def booking_cancel(self, request):
        serializer = CancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data.get('id', None)
        uid = serializer.validated_data.get('uid', None)
        kwargs = {}
        if id:
            kwargs['id'] = id
        else:
            kwargs['uid'] = uid
        calendardb = CalendarDb.objects.filter(**kwargs).get()
        calendardb.cancel_appointment()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @rest_framework.decorators.detail_route(methods=['post', 'get'])
    def add_to_ical_outlook(self, request, *args, **kwargs):
        calendar_obj = self.get_object()
        response = HttpResponse(calendar_obj.make_vobject,
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
        return response

    @rest_framework.decorators.list_route(methods=['post'])
    def add_additional_time_mass(self, request):
        choice_list = {
            'weekly': self.every_day_of_week,
            'biweekly': self.every_day_of_week2,
            'triweekly': self.every_day_of_week3,
            'quadweekly': self.every_day_of_week4,
            'monthly': self.every_date_month,
            'monthly-day': self.every_2end_date_month
        }
        serializer = RecurringAddDateMassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data.get('date', None)
        type = serializer.validated_data.get('type', None)
        count = serializer.validated_data.get('count', None)
        new = []
        for lines in choice_list[type](date, count):
            new.append({
                'time': lines,
                'date': lines,
                'choice': False,
                'block': False,
                'datetime': lines,
                'key': lines.strftime('%s')
            })
        serializer = RecurringResponseDateSerializer(data={'date': new})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @rest_framework.decorators.list_route(methods=['post'])
    def filter_appointment(self, request):
        serializer = FilterAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calendar_obj = serializer.validated_data.get('calendar_obj')
        return Response(CalendarDbFullModelSerializer(calendar_obj, many=True).data, status=status.HTTP_200_OK)

    @rest_framework.decorators.list_route(methods=['post'], permission_classes=[IsAuthenticated, ])
    def get_main_calendar_from_date(self, request):
        serializer = GetDateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date_obj = serializer.validated_data.get('date')
        end_date_obj = serializer.validated_data.get('end_date')

        true_first_date = datetime.datetime.combine(
            date_obj, datetime.datetime.min.time(), tzinfo=pytz.utc)
        if end_date_obj:
            true_last_date = datetime.datetime.combine(
                end_date_obj, datetime.datetime.max.time(), tzinfo=pytz.utc)
        else:
            true_last_date = true_first_date + datetime.timedelta(days=31)

        calendar_list_obj = self.queryset.filter(
            generalsettings_id=request.user.generalsettings_id,
            start_datetime__range=[true_first_date, true_last_date]
        ).active_appointments().select_related('users_customer', 'services').order_by('start_datetime')

        return Response(
            CalendarDbMainFullModelSerializer(
                calendar_list_obj, many=True, ).data
        )

    @rest_framework.decorators.list_route(methods=['post'])
    def save_calendar_appointment(self, request):
        logger.info("Received request to save calendar appointment")
        serializer = SaveCalendarAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @rest_framework.decorators.list_route(methods=['post'])
    def import_appointments(self, request):
        service_id_list = request.data.get('service_id', '')
        start_date_time_list = request.data.get('start_date_time', '')
        end_date_time_list = request.data.get('end_date_time', '')
        name_list = request.data.get('name', '')
        last_name_list = request.data.get('last_name', '')
        email_list = request.data.get('email', '')
        phone_list = request.data.get('phone', '')
        note_list = request.data.get('note', '')
        generalsettings = request.user.generalsettings_id
        num_of_records = request.data.get('num_of_records', None)
        provider_id = request.data.get('provider_id', None)

        for index in range(0, num_of_records):
            try:
                service = service_id_list[index]
            except:
                service = None
            try:
                start_date_time = start_date_time_list[index]
                start_date_time = datetime.datetime.strptime(
                    start_date_time, '%m/%d/%Y %I:%M %p')
            except:
                start_date_time = None
            try:
                end_date_time = end_date_time_list[index]
                end_date_time = datetime.datetime.strptime(
                    end_date_time, '%m/%d/%Y %I:%M %p')
            except:
                end_date_time = None
            try:
                first_name = name_list[index]
            except:
                first_name = None
            try:
                last_name = last_name_list[index]
            except:
                last_name = None
            try:
                email = email_list[index]
            except:
                email = None
            try:
                phone = phone_list[index]
            except:
                phone = None
            try:
                note = note_list[index]
            except:
                note = None

            users_provider_obj: Account = get_object_or_404(
                Account, id=provider_id)
            services_obj = Service.objects.filter(name=service).first()
            if not services_obj:
                return Response({'status': 'service not found'}, status=status.HTTP_404_NOT_FOUND)

            account_obj: Account = Account.get_customer(
                users_provider_obj.generalsettings_id, email=email, phone=phone)

            if account_obj:
                # update the customer data
                account_obj.username = email
                account_obj.name = first_name
                account_obj.last_name = last_name
                account_obj.phone = phone
                account_obj.note = note
                account_obj.save()
            else:
                # check that the mail ID is safe to be used for new user
                if email:
                    if Account.registered_with_email_id(
                            email_id=email,
                            company_id=users_provider_obj.generalsettings_id,
                    ):
                        return Response({'status': 'email error'}, status=status.HTTP_404_NOT_FOUND)
                    # create customer record for the provider
                    try:
                        account_obj = Account.objects.create(
                            email=email,
                            name=first_name,
                            last_name=last_name,
                            phone=phone,
                            note=note,
                            is_customers=True,
                            generalsettings=users_provider_obj.generalsettings
                        )
                    except IntegrityError as e:
                        print(e)
                else:
                    try:
                        account_obj = Account.objects.create(
                            name=first_name,
                            last_name=last_name,
                            phone=phone,
                            note=note,
                            is_customers=True,
                            generalsettings=users_provider_obj.generalsettings
                        )
                    except IntegrityError as e:
                        print(e)
            
            if start_date_time and end_date_time:
                # start_date_time = utils.parse_datetime(start_date_time).replace(tzinfo=None)
                # end_date_time = utils.parse_datetime(end_date_time).replace(tzinfo=None)

                CalendarDb.add_or_reschedule_appointment(
                    provider=users_provider_obj,
                    customer=account_obj,
                    start_time=start_date_time,
                    service=services_obj,
                    end_time=end_date_time,
                    note=note,
                    appointment_id=None,
                    rasa_bot=None,
                    is_import_appt=True
                ),

            # calendardb = CalendarDb()
            # calendardb.users_provider = users_provider_obj
            # calendardb.users_customer = account_obj
            # calendardb.services = services_obj
            # calendardb.notes = note

            # if start_date_time and end_date_time:
            #     calendardb.start_datetime = timezone.localtime(
            #         (start_date_time.replace(tzinfo=None)).astimezone())
            #     calendardb.end_datetime = timezone.localtime(
            #         (end_date_time.replace(tzinfo=None)).astimezone())
            #     calendardb.save()

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # send emails and remove google calendar events
            from . import tasks
            # tasks.async_run_calendar_func(instance.id, 'send_cancellation_email')
            tasks.add_to_google_calendar_task(
                calendar_pk=instance.id, remove=True, overide_delete=True)
            # self.perform_destroy(instance)
        except:
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)
