from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage

from .models import GoogleCredentials, SIGNER, Account


def _get_flow(request):
    redirect_uri = (request.build_absolute_uri('/auth/oauth2callback'))
    return flow_from_clientsecrets(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=redirect_uri)


def get_authorize_url(request: HttpRequest):
    FLOW = _get_flow(request)
    FLOW.params['access_type'] = 'offline'
    FLOW.params['prompt'] = 'consent'
    FLOW.params['state'] = SIGNER.dumps({
        'user_id': request.user.pk,
        'return_url': request.META.get('HTTP_REFERER', 'https://app.bookedfusion.com/')
    })
    return FLOW.step1_get_authorize_url()


def auth_return(request):
    data = SIGNER.loads(request.GET['state'], max_age=500)
    if not data:
        return HttpResponseBadRequest()
    user_id = data['user_id']
    user = get_object_or_404(Account, id=user_id)
    FLOW = _get_flow(request)
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(GoogleCredentials, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponse('''
    <script type="text/javascript">window.opener.postMessage('authSuccess', '*');window.close();</script>
    ''')


@login_required
def index(request):
    storage = DjangoORMStorage(GoogleCredentials, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        authorize_url = get_authorize_url(request)
        return HttpResponseRedirect(authorize_url)
    else:
        return JsonResponse({
            'token': credential.refresh_token,
        })
