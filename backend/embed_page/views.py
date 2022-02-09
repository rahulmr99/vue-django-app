import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from app_settings.models import GeneralSettings
from app_settings.utils import reverse_fullurl
from authentication_user.models import Account
from calendar_manager.models import CalendarDb


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return '', ''

    if day_diff == 0:
        if second_diff < 10:
            return "Recently booked an appointment", "just now"
        if second_diff < 60:
            return "Recently booked an appointment",  str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "Recently booked an appointment", "a minute ago"
        if second_diff < 3600:
            return "Recently booked an appointment", str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "Recently booked an appointment", "an hour ago"
        if second_diff < 86400:
            return "Recently booked an appointment", str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Booked an appointment", "Yesterday"
    if day_diff < 7:
        return "Booked an appointment", str(int(day_diff)) + " days ago"
    if day_diff < 31:
        return "Booked an appointment", str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return "Booked an appointment", str(int(day_diff / 30)) + " months ago"
    return "Booked an appointment", str(int(day_diff / 365)) + " years ago"


@method_decorator(xframe_options_exempt, name='dispatch')
class EmbeddableBookingPage(TemplateView):
    template_name = 'embed_page/index.html'

    def dispatch(self, *args, **kwargs):
        response = super(EmbeddableBookingPage, self).dispatch(*args, **kwargs)
        # Remove iframe same origin header so that we can embed booking page on any domain
        del response['X-Frame-Options']
        return response

    def get_context_data(self, **kwargs):
        fltrs = ({'id': kwargs['company_id']}
                 if 'company_id' in kwargs
                 else {'slug': kwargs['company_slug']})
        company = get_object_or_404(GeneralSettings, **fltrs)
        kwargs['providers'] = providers = Account.objects.filter(
            is_provider=True, services__isnull=False,
            generalsettings=company).distinct()

        if providers.count() == 1:
            provider = providers.first()
            kwargs['services'] = provider.services.all()
            kwargs['provider_id'] = provider.id
        return super(EmbeddableBookingPage, self).get_context_data(**kwargs)


@method_decorator(xframe_options_exempt, name='dispatch')
class EmbeddableScript(TemplateView):
    template_name = 'embed_page/embedder.js'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['domain_name'] = reverse_fullurl()
        return ctx


@method_decorator(xframe_options_exempt, name='dispatch')
class EmbeddablePopupScript(TemplateView):
    template_name = 'embed_page/popup_embedder.js'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['domain_name'] = reverse_fullurl()
        return ctx


@csrf_exempt
@method_decorator(xframe_options_exempt, name='dispatch')
def embeddable_popup_page(request):
    template_name = 'embed_page/popup_embedder.html'
    return render(request, template_name, {
        "customer": request.GET['customer'],
        "from": request.GET['from'],
        "booked": request.GET['booked'],
        "when": request.GET['when'],
    })


@csrf_exempt
@method_decorator(xframe_options_exempt, name='dispatch')
def embeddable_popup_json(request, general_setting_id):
    # put this in db?
    phone_code_dict = {
        '201': 'New Jersey',
        '202': 'Washington,DC',
        '203': 'Connecticut',
        '205': 'Alabama',
        '206': 'Washington',
        '207': 'Maine',
        '208': 'Idaho',
        '209': 'California',
        '210': 'Texas',
        '212': 'New York',
        '213': 'California',
        '214': 'Texas',
        '215': 'Pennsylvania',
        '216': 'Ohio',
        '217': 'Illinois',
        '218': 'Minnesota',
        '219': 'Indiana',
        '224': 'Illinois',
        '225': 'Louisiana',
        '227': 'Maryland',
        '228': 'Mississippi',
        '229': 'Georgia',
        '231': 'Michigan',
        '234': 'Ohio',
        '239': 'Florida',
        '240': 'Maryland',
        '248': 'Michigan',
        '251': 'Alabama',
        '252': 'North Carolina',
        '253': 'Washington',
        '254': 'Texas',
        '256': 'Alabama',
        '260': 'Indiana',
        '262': 'Wisconsin',
        '267': 'Pennsylvania',
        '269': 'Michigan',
        '270': 'Kentucky',
        '276': 'Virginia',
        '281': 'Texas',
        '283': 'Ohio',
        '301': 'Maryland',
        '302': 'Delaware',
        '303': 'Colorado',
        '304': 'West Virginia',
        '305': 'Florida',
        '307': 'Wyoming',
        '308': 'Nebraska',
        '309': 'Illinois',
        '310': 'California',
        '312': 'Illinois',
        '313': 'Michigan',
        '314': 'Missouri',
        '315': 'New York',
        '316': 'Kansas',
        '317': 'Indiana',
        '318': 'Louisiana',
        '319': 'Iowa',
        '320': 'Minnesota',
        '321': 'Florida',
        '323': 'California',
        '330': 'Ohio',
        '331': 'Illinois',
        '334': 'Alabama',
        '336': 'North Carolina',
        '337': 'Louisiana',
        '339': 'Massachusetts',
        '347': 'New York',
        '351': 'Massachusetts',
        '352': 'Florida',
        '360': 'Washington',
        '361': 'Texas',
        '386': 'Florida',
        '401': 'Rhode Island',
        '402': 'Nebraska',
        '404': 'Georgia',
        '405': 'Oklahoma',
        '406': 'Montana',
        '407': 'Florida',
        '408': 'California',
        '409': 'Texas',
        '410': 'Maryland',
        '412': 'Pennsylvania',
        '413': 'Massachusetts',
        '414': 'Wisconsin',
        '415': 'California',
        '417': 'Missouri',
        '419': 'Ohio',
        '423': 'Tennessee',
        '424': 'California',
        '425': 'Washington',
        '434': 'Virginia',
        '435': 'Utah',
        '440': 'Ohio',
        '443': 'Maryland',
        '445': 'Pennsylvania',
        '464': 'Illinois',
        '469': 'Texas',
        '470': 'Georgia',
        '475': 'Connecticut',
        '478': 'Georgia',
        '479': 'Arkansas',
        '480': 'Arizona',
        '484': 'Pennsylvania',
        '501': 'Arkansas',
        '502': 'Kentucky',
        '503': 'Oregon',
        '504': 'Louisiana',
        '505': 'New Mexico',
        '507': 'Minnesota',
        '508': 'Massachusetts',
        '509': 'Washington',
        '510': 'California',
        '512': 'Texas',
        '513': 'Ohio',
        '515': 'Iowa',
        '516': 'New York',
        '517': 'Michigan',
        '518': 'New York',
        '520': 'Arizona',
        '530': 'California',
        '540': 'Virginia',
        '541': 'Oregon',
        '551': 'New Jersey',
        '557': 'Missouri',
        '559': 'California',
        '561': 'Florida',
        '562': 'California',
        '563': 'Iowa',
        '564': 'Washington',
        '567': 'Ohio',
        '570': 'Pennsylvania',
        '571': 'Virginia',
        '573': 'Missouri',
        '574': 'Indiana',
        '580': 'Oklahoma',
        '585': 'New York',
        '586': 'Michigan',
        '601': 'Mississippi',
        '602': 'Arizona',
        '603': 'New Hampshire',
        '605': 'South Dakota',
        '606': 'Kentucky',
        '607': 'New York',
        '608': 'Wisconsin',
        '609': 'New Jersey',
        '610': 'Pennsylvania',
        '612': 'Minnesota',
        '614': 'Ohio',
        '615': 'Tennessee',
        '616': 'Michigan',
        '617': 'Massachusetts',
        '618': 'Illinois',
        '619': 'California',
        '620': 'Kansas',
        '623': 'Arizona',
        '626': 'California',
        '630': 'Illinois',
        '631': 'New York',
        '636': 'Missouri',
        '641': 'Iowa',
        '646': 'New York',
        '650': 'California',
        '651': 'Minnesota',
        '660': 'Missouri',
        '661': 'California',
        '662': 'Mississippi',
        '667': 'Maryland',
        '678': 'Georgia',
        '682': 'Texas',
        '701': 'North Dakota',
        '702': 'Nevada',
        '703': 'Virginia',
        '704': 'North Carolina',
        '706': 'Georgia',
        '707': 'California',
        '708': 'Illinois',
        '712': 'Iowa',
        '713': 'Texas',
        '714': 'California',
        '715': 'Wisconsin',
        '716': 'New York',
        '717': 'Pennsylvania',
        '718': 'New York',
        '719': 'Colorado',
        '720': 'Colorado',
        '724': 'Pennsylvania',
        '727': 'Florida',
        '731': 'Tennessee',
        '732': 'New Jersey',
        '734': 'Michigan',
        '737': 'Texas',
        '740': 'Ohio',
        '754': 'Florida',
        '757': 'Virginia',
        '760': 'California',
        '763': 'Minnesota',
        '765': 'Indiana',
        '770': 'Georgia',
        '772': 'Florida',
        '773': 'Illinois',
        '774': 'Massachusetts',
        '775': 'Nevada',
        '781': 'Massachusetts',
        '785': 'Kansas',
        '786': 'Florida',
        '801': 'Utah',
        '802': 'Vermont',
        '803': 'South Carolina',
        '804': 'Virginia',
        '805': 'California',
        '806': 'Texas',
        '808': 'Hawaii',
        '810': 'Michigan',
        '812': 'Indiana',
        '813': 'Florida',
        '814': 'Pennsylvania',
        '815': 'Illinois',
        '816': 'Missouri',
        '817': 'Texas',
        '818': 'California',
        '828': 'North Carolina',
        '830': 'Texas',
        '831': 'California',
        '832': 'Texas',
        '835': 'Pennsylvania',
        '843': 'South Carolina',
        '845': 'New York',
        '847': 'Illinois',
        '848': 'New Jersey',
        '850': 'Florida',
        '856': 'New Jersey',
        '857': 'Massachusetts',
        '858': 'California',
        '859': 'Kentucky',
        '860': 'Connecticut',
        '862': 'New Jersey',
        '863': 'Florida',
        '864': 'South Carolina',
        '865': 'Tennessee',
        '870': 'Arkansas',
        '872': 'Illinois',
        '878': 'Pennsylvania',
        '901': 'Tennessee',
        '903': 'Texas',
        '904': 'Florida',
        '906': 'Michigan',
        '907': 'Alaska',
        '908': 'New Jersey',
        '909': 'California',
        '910': 'North Carolina',
        '912': 'Georgia',
        '913': 'Kansas',
        '914': 'New York',
        '915': 'Texas',
        '916': 'California',
        '917': 'New York',
        '918': 'Oklahoma',
        '919': 'North Carolina',
        '920': 'Wisconsin',
        '925': 'California',
        '928': 'Arizona',
        '931': 'Tennessee',
        '936': 'Texas',
        '937': 'Ohio',
        '940': 'Texas',
        '941': 'Florida',
        '947': 'Michigan',
        '949': 'California',
        '952': 'Minnesota',
        '954': 'Florida',
        '956': 'Texas',
        '959': 'Connecticut',
        '970': 'Colorado',
        '971': 'Oregon',
        '972': 'Texas',
        '973': 'New Jersey',
        '975': 'Missouri',
        '978': 'Massachusetts',
        '979': 'Texas',
        '980': 'North Carolina',
        '984': 'North Carolina',
        '985': 'Louisiana',
        '989': 'Michigan',
    }
    start_date = datetime.datetime.now() + datetime.timedelta(-30)

    calender_db_objects = CalendarDb.objects.filter(
        generalsettings_id=general_setting_id,
        book_datetime__gte=start_date,
        book_datetime__lte=datetime.datetime.now(),
    )

    calender_db_dict = dict()
    iterator = 1
    for i in calender_db_objects:
        if i.users_customer_id:
            phone_code = i.users_customer.phone[:3] if i.users_customer_id and i.users_customer.phone else None
            whereami = 'Somewhere'
            d_then = i.book_datetime

            if phone_code in phone_code_dict:
                whereami = phone_code_dict[phone_code]

            booked, when = pretty_date(d_then)
            calender_db_dict[iterator] = {
                'customer': i.users_customer.name,
                'from': whereami,
                'booked': booked,
                'when': when,
            }
            iterator = iterator + 1
    return JsonResponse(calender_db_dict)
