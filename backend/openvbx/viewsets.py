import json
import requests
from django.conf import settings
from django.http import Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from twilio.jwt.client import ClientCapabilityToken
from twilio.rest import Client

from api_v1.pagination import StandardResultsSetPagination
from app_settings.models import TwilioAccount
from authentication_user.mixins import GetGenSettingsMixin
from openvbx.utils import get_client_name, get_booked_fusion_number
from . import models, serializers


class GetTokenAPI(APIView):
    """
    api to get token for the user requesting
    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, company_id):
        """
        Return a list of all users.
        """
        identity = get_client_name(company_id)
        capability = ClientCapabilityToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN)
        capability.allow_client_outgoing(settings.TWILIO_APPLICATION_SID)
        capability.allow_client_incoming(identity)
        token = capability.to_jwt()
        return Response({'token': token.decode(), 'identity': identity})


class VoiceMailViewset(GetGenSettingsMixin, ModelViewSet):
    queryset = models.VoiceMail.objects.filter()
    serializer_class = serializers.VoiceMailSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ['created', ]


class VoiceMailConfigViewset(GetGenSettingsMixin, ModelViewSet):
    queryset = models.VoiceMailConfig.objects.filter()
    serializer_class = serializers.VoiceMailConfigSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticated,)


class GetPhoneNumbers(APIView):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    def get(self, request, *args, **kwargs):
        account_sid = self.account_sid
        auth_token = self.auth_token

        countrycode = request.GET.get('countrycode').upper()
        areacode = request.GET.get('areacode')
        number_list = []

        if not countrycode:
            countrycode = 'US'
        try:
            client = Client(account_sid, auth_token)
            if areacode:
                numbers = client.available_phone_numbers(countrycode) \
                    .local \
                    .list(area_code=areacode)
            else:
                numbers = client.available_phone_numbers(countrycode) \
                    .local \
                    .list()
            for number in numbers:
                number_list.append({'phone numbers': number.phone_number})
        except Exception as e:
            return Response({'error': e.args[1].content})
        return Response({'number_list': number_list})

    def post(self, request, *args, **kwargs):
        account_sid = self.account_sid
        auth_token = self.auth_token
        client = Client(account_sid, auth_token)
        phone_number = request.data.get('number')
        company_id = self.request.user.generalsettings.pk
        if phone_number:
            try:
                sub_account = client.api.accounts.create(friendly_name=self.request.user.get_full_name())
                
                # 1 ------------------------------------------------------------
                # Once twilio number is generated create bot for this number
                # In multibot, Each bot runs in different port.
                # Set webhook with the given port from the bot server
                
                # 2 ------------------------------------------------------------
                # Each number is activated and it will created a new subaccount in twilio
                # Each subaccount have unique sid and authtoken
                # Lets pass those sid and authtoken also to the bot server.
                
                # 3 ------------------------------------------------------------
                # Bot and user convertation is whole pushes to the chat service
                # Inorder to do that first we need to create a chat service
                # Then pass the service id to the bot

                # 4 -------------------------------------------------------------------
                # Set role permission for delete channel

                # 5 -------------------------------------------------------------------
                # Set a webhook for message sent post event after chat service creation
                # We need to inform the user when a message receives in chat

                account_sid = sub_account.sid
                auth_token = sub_account.auth_token

                # Create chat service
                client = Client(account_sid, auth_token)
                service = client.chat.services.create(friendly_name='Receptionist')
                
                # Allow channel user to delete the channel
                roles = client.chat.services(service.sid).roles.list(limit=20)
                for record in roles:
                    if record.friendly_name == 'channel user':
                        client.chat.services(service.sid).roles(record.sid).update(permission=["destroyChannel","sendMessage", "leaveChannel", "addMember"])

                # Setting webhook in chat service
                post_webhook_url = '{}/rasa-bot/sms/user/send-sms/'.format(settings.TWILIO_WEBHOOK_BASE_URL)
                response = requests.post('https://chat.twilio.com/v1/Services/{}'.format(service.sid), \
                                data = {'PostWebhookUrl':post_webhook_url,'WebhookMethod':'POST','WebhookFilters':'onMessageSent'}, 
                                auth=(str(sub_account.sid),str(sub_account.auth_token)))
                
                data = json.dumps({"accountSid":str(sub_account.sid), "authToken":str(sub_account.auth_token), "number":str(phone_number), "serviceId":str(service.sid)})
                headers = {'Content-Type': 'application/json'}
                url = '{}/create'.format(settings.BOTKIT_SERVER_URL)
                response = requests.post(url, data=data, headers=headers)
                data = response.json()

                sub_account_client = Client(sub_account.sid, sub_account.auth_token)
                number = sub_account_client.incoming_phone_numbers \
                    .create(
                    phone_number=phone_number,
                    # voice_url='{}/bot/voice/{}/'.format(settings.TWILIO_WEBHOOK_BASE_URL, company_id),
                    voice_fallback_url='{}/ivrs/caller-vr/{}/'.format(settings.TWILIO_WEBHOOK_BASE_URL, company_id),
                    # sms_url='{}/bot/sms/{}/'.format(settings.TWILIO_WEBHOOK_BASE_URL, company_id),
                    sms_url='{}:{}/sms/receive/'.format(settings.BOTKIT_SERVER_DOMAIN, data['port']),
                    identity_sid=sub_account.sid
                )
                client = Client(account_sid, auth_token)
                new_key = client.new_keys.create()
                
                TwilioAccount.objects.create(booked_fusion_number=number.phone_number,
                                             sid=number.sid,
                                             account_sid=account_sid,
                                             auth_token=auth_token,
                                             service_id=service.sid,
                                             api_key=new_key.sid,
                                             api_key_secret=new_key.secret,
                                             generalsettings=self.request.user.generalsettings)
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)

        return Response({'status': str(e)}, status=status.HTTP_404_NOT_FOUND)


class GetIsTwilioNumberPresent(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        generalsettings_id = request.GET.get('id')
        if not str(generalsettings_id).isdigit():
            raise Http404
        res = get_booked_fusion_number(generalsettings_id)
        return Response(res)
