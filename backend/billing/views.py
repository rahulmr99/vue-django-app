from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authentication_user.models import Account
from billing.utils import rollback_customer
from openvbx.utils import get_booked_fusion_number
from .serializers import RegisterUserSerializer, SubscriptionSerializer, AccountSerializer
from .utils import (
    ChargebeeError,
    create_subscription,
    get_subscription,
    cancel_subscription,
    check_status,
    reactivate_subscription
)
from authentication_user.serializers import AccountModelSerializer

from mailer.utils import send_mail_using_template_name


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        # Just doing validation here..
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class SubscriptionView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SubscriptionSerializer

    def post(self, request, format=None):
        account = Account()
        data = request.data.copy()
        account.init_generalsettings_id(data['email'])
        data['generalsettings'] = account.generalsettings_id
        data['is_active'] = True
        data['name'] = request.data.get('first_name')
        serializer = AccountModelSerializer(instance=account, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.set_password(serializer.validated_data['password'])
        serializer.instance.is_provider = True
        serializer.instance.is_admin = True
        serializer.instance.save()
        serializer.instance.create_default_working_pan()

        try:
            create_subscription(account, request.data.get('plan_id'), request.data.get('stripe_token'))
        except ChargebeeError as e:
            rollback_customer(account)
            return Response({'status': 'error', 'reason': str(e), 'message': str(e.exact)},
                            status=status.HTTP_400_BAD_REQUEST)

        send_mail_using_template_name('Welcome to BookedFusion!', dict(name=account.email),
                                      'mailer/billing_confirmation.html', account.email, )
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class CancelSubscriptionView(APIView):
    serializer_class = AccountSerializer

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.id != serializer.validated_data['account_id']:
            return Response({'status': 'error',
                             'reason': 'Not Authorized',
                             'message': 'You do not have permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            end_at = cancel_subscription(serializer.validated_data['account_id'])
            return Response({'status': 'ok', 'end_at': end_at}, status=status.HTTP_200_OK)
        except ChargebeeError as e:
            return Response({'status': 'error', 'reason': str(e), 'message': str(e.exact)},
                            status=status.HTTP_400_BAD_REQUEST)


class FetchSubscriptionView(APIView):
    def get(self, request, account_id, format=None):
        if request.user.id != int(account_id):
            return Response({'status': 'error',
                             'reason': 'Not Authorized',
                             'message': 'You do not have permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            subscription = get_subscription(account_id)
        except ChargebeeError as e:
            return Response({'status': 'error', 'reason': str(e), 'message': str(e.exact)},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(subscription, status=status.HTTP_200_OK)


class StatusSubscription(APIView):
    def get(self, request):
        try:
            subscription = get_subscription(request.user.id)
        except ChargebeeError as e:
            return Response({'status': 'error', 'reason': str(e), 'message': str(e.exact)},
                            status=status.HTTP_400_BAD_REQUEST)

        subscription_data = {
            'plan_id': subscription.get('plan_id'),
            'start_trial_time': subscription.get('trial_start'),
            'end_trial_time': subscription.get('trial_end'),
            'cancelled_time': subscription.get('cancelled_at', False),
            'next_billing': subscription.get('next_billing_at', False),
        }
        subscription_data.update(check_status(subscription['status']))
        subscription_data.update(get_booked_fusion_number(request.user.generalsettings.pk))
        return Response(subscription_data, status=status.HTTP_200_OK)


class ReactivateSubscription(APIView):
    serializer_class = AccountSerializer

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.id != serializer.validated_data['account_id']:
            return Response({'status': 'error',
                             'reason': 'Not Authorized',
                             'message': 'You do not have permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            reactivate_at = reactivate_subscription(serializer.validated_data['account_id'])
            return Response({'status': 'ok', 'reactivated_at': reactivate_at}, status=status.HTTP_200_OK)
        except ChargebeeError as e:
            return Response({'status': 'error', 'reason': str(e), 'message': str(e.exact)},
                            status=status.HTTP_400_BAD_REQUEST)
