import pytz
import json
import requests
from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings

from dateutil.parser import parse

from api_v1.pagination import StandardResultsSetPagination
from authentication_user.mixins import GetGenSettingsMixin
from authentication_user.models import Account, ConfirmationCode, GoogleCredentials, CustomerAccount
from authentication_user.permissions import IsCreationOrIsAuthenticated
from authentication_user.views import get_authorize_url
from calendar_manager.models import CalendarDb
from mailer.utils import send_mail_using_template_name
from services.models import Service
from .serializers import (AccountModelSerializer, RegisterUserSerializer, CreateCustomerSerializer,
                          UpdateCalendarSerializer, UpdatePasswordSerializer, PublicProvidersModelSerializer,
                          ConfirmPasswordReset,
                          CheckEmailExistsSerializer, CustomerModelSerializer, CustomerModelWithoutUniqueValidatorSerializer)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data.get('account_obj', None)
        email = serializer.validated_data.get('email', None)
        password = serializer.validated_data.get('password1', None)
        if account:
            account.set_password(password)
            account.save()
        else:
            Account.objects.create_customer(email, password)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class EmailConfirmationCode(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """email confirmation code if the account exists"""
        serializer = CheckEmailExistsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_id = serializer.validated_data.get('email')

        # get token
        code = ConfirmationCode.generate_confirm_code(email_id)
        account = Account.objects.get_by_natural_key(email_id)

        # send email async
        send_mail_using_template_name('Confirmation code', dict(name=account.name, code=code),
                                      'mailer/confirmation_code.html', email_id, )

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ConfirmPasswordReset(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data['account']
        account.set_password(serializer.validated_data['password'])
        account.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


def jwt_response_payload_handler(token, user: Account = None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    user_serializer = PublicProvidersModelSerializer(instance=user)
    return {
        'token': token,
        'status': user.is_active,
        'info': user_serializer.data
    }


class AccountModelViewSet(GetGenSettingsMixin, ModelViewSet, ):
    queryset = Account.objects.filter()
    serializer_class = AccountModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsCreationOrIsAuthenticated,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend,)
    search_fields = (
        'username', 'name', 'last_name', 'email', 'phone', 'mobile', 'address', 'state', 'city', 'zip_code', 'note'
    )
    ordering_fields = '__all__'
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        """signup activity. Only should be used to create provider accounts"""
        data = request.data.copy()

        account = Account()
        account.init_generalsettings_id(data['email'])

        data['generalsettings'] = account.generalsettings_id
        data['is_active'] = True

        serializer = self.serializer_class(instance=account, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.set_password(serializer.validated_data['password'])
        serializer.instance.save()

        return Response({}, status=status.HTTP_201_CREATED)

    @list_route(['get'])
    def get_gauth_link(self, request):
        # login the current user to the session, so that we later get the user from session
        return Response({'url': get_authorize_url(request)})

    @list_route(methods=['delete'], )
    def revoke_google_credentials(self, request):
        """if there is no credentials available for the user then redirect to the page"""
        credential = GoogleCredentials.objects.filter(id=request.user).first()
        if credential:
            credential.delete()
        return Response({'status': 'enabled'})

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def get_providers(self, request):
        providers = self.get_queryset().filter(
            is_provider=True,
            services__isnull=False,
        ).distinct()
        serializer = PublicProvidersModelSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Created separate API. May need to remove this.
    @list_route(methods=['get'])
    def get_customers(self, request):
        accounts = CustomerAccount.objects.filter()
        serializer = AccountModelSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def update_calendar(self, request):
        serializer = UpdateCalendarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        calendar_id = serializer.validated_data.get('calendar_id', None)
        datetime = serializer.validated_data.get('datetime', None)
        service = serializer.validated_data.get('service', None)

        service_obj = Service.objects.get(id=service)
        tzname = serializer.validated_data.get('timezone', None)

        calendardb = get_object_or_404(CalendarDb, id=calendar_id)
        calendardb.set_times(datetime, service=service_obj, tzname=tzname)
        calendardb.save()

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def update_password(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password1', None)
        account = serializer.validated_data.get('account_obj', None)

        # check the user requesting belong to the same company
        account.check_account_access(request.user)
        account.set_password(password)
        account.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_providers_private(self, request):
        """
            return provider data from the same company as the user requesting
        Args:
            request:

        Returns:

        """
        providers = self.get_queryset().filter(is_provider=True, )
        serializer = PublicProvidersModelSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def add_customers(self, request):
        name_list = request.data.get('name', '')
        last_name_list = request.data.get('last_name', '')
        email_list = request.data.get('email', '')
        phone_list = request.data.get('phone', '')
        note_list = request.data.get('note', '')
        generalsettings = request.user.generalsettings_id
        num_of_records = request.data.get('num_of_records', None)

        for index in range(0, num_of_records):
            try:
                name = name_list[index]
            except:
                name = None
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

            try:
                patient = Account.objects.create(name=name, last_name=last_name, email=email, phone=phone, note=note,
                                                 is_customers=True, generalsettings_id=generalsettings)
            except Exception as e:
                print(e)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def getCaller(self, request):
        number = request.GET.get('number')
        try:
            customer = CustomerAccount.objects.get(phone=number)
        except:
            customer = None
        if customer == None:
            try:
                customer = CustomerAccount.objects.get(mobile=number)
            except:
                customer = None
        if not customer == None:
            serializer = AccountModelSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomersModelViewSet(AccountModelViewSet):
    serializer_class = CustomerModelSerializer

    def get_queryset(self):
        return CustomerAccount.objects.filter(generalsettings=self.request.user.generalsettings)

    def create_appointment(self, data: dict, customer_account: Account):

        if(data.get('datetime', None)):
            datetime = parse(data.get('datetime', '')).replace(tzinfo=None)
        else:
            datetime = None

        provider = data.get('provider', '')
        service = data.get('service', '')

        if provider and datetime and service:
            provider_obj = Account.objects.get(id=provider)
            service_obj = Service.objects.get(id=service)
            calendardb = CalendarDb.add_or_reschedule_appointment(
                provider=provider_obj,
                customer=customer_account,
                service=service_obj,
                start_time=datetime,
            )
            return calendardb

    def convert_date_time_timezone(self, calendar_obj):
        tzname = 'US/Eastern' if calendar_obj.users_provider.timezone and calendar_obj.users_provider.timezone == 'EST' else calendar_obj.users_provider.timezone
        tz_obj = pytz.timezone(tzname)
        # timezone.activate(tz_obj)

        appt_date = calendar_obj.start_datetime.astimezone(tz_obj)
        day_string = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        if appt_date:
            month = appt_date.strftime("%b")
            date = appt_date.strftime("%d")
            time = appt_date.strftime("%I:%M %p")
            day = appt_date.weekday()

            return day_string[day], date, month, time

    def create(self, request, *args, **kwargs):
        serializer = CustomerModelWithoutUniqueValidatorSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        last_name = serializer.validated_data.get('last_name')
        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email') or None
        note = serializer.validated_data.get('note')

        generalsettings_id = (
            serializer.validated_data.get('generalsettings')
            or (self.request.user.generalsettings_id if self.request.user.is_authenticated else None)
        )

        if not generalsettings_id:
            raise Http404
        else:
            generalsettings_id = generalsettings_id.id

        account = Account.get_customer(
            generalsettings_id, email=email, phone=phone)

        if not account:
            # check that the user could create new account
            if email:
                if Account.registered_with_email_id(
                        email_id=email,
                        company_id=generalsettings_id,
                ):
                    raise ValidationError(
                        {'error': "This E-Mail ID is already registered with us."})

                if Account.objects.filter(
                    generalsettings_id=generalsettings_id,
                    phone=phone
                ).exists():
                    raise ValidationError(
                        {'error': "Phone Number is already exist."})

            account = Account.objects.create_customer(
                email=email,
                password=None,
                name=name,
                last_name=last_name,
                phone=phone,
                generalsettings_id=generalsettings_id,
                is_active=None,
                note=note,
            )

        account.country = serializer.validated_data.get('country')
        # account.country_code = country_code
        account.name = name
        account.last_name = last_name
        account.phone = phone

        try:
            account.save()
        except IntegrityError:
            raise ValidationError(
                {'error': "Email and Phone number already exist."})

        token = ''
        if not request.user.is_authenticated:
            # create a JWT token and send to customer
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(account)
            token = jwt_encode_handler(payload)

        response = {'token': token}
        calendar_obj = self.create_appointment(
            request.data, customer_account=account)
        if calendar_obj:
            response['id'] = calendar_obj.pk
            response['google_calendar_link'] = calendar_obj.get_google_calendar_link(
                True)
            response['booking_message'] = "Your appointment with {} {}".format(
                calendar_obj.users_provider.name, calendar_obj.users_provider.last_name)
            response['email'] = calendar_obj.users_customer.email
            day, date, month, time = self.convert_date_time_timezone(
                calendar_obj)
            response['booking_date'] = date
            response['booking_month'] = month
            response['booking_day'] = day
            response['booking_time'] = time
            response['booking_service'] = calendar_obj.services.name
        return Response(response, status=status.HTTP_200_OK)

    # delete patinet and also their appointments
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = json.dumps({"user": str(instance.full_phone_number)})
            headers = {'Content-Type': 'application/json'}
            url = '{}/patient'.format(settings.BOTKIT_SERVER_URL)
            response = requests.delete(url, data=data, headers=headers)
            CalendarDb.objects.filter(users_customer=instance).delete()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
