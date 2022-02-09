from django.conf.urls import url

from .views import *
from .apps import LexbotConfig

app_name = LexbotConfig.name

urlpatterns = [
    url(r'^sms/(?P<company_id>\d+)/$', sms_bot_view, name='sms_bot_view'),
    url(r'^voice/(?P<company_id>\d+)/$', voice_bot_view, name='voice_bot_view'),
    url(r'^voice/(?P<company_id>\d+)/choose/$', get_voice_bot_user_choice, name='get_voice_bot_user_choice'),
    url(r'^voice/(?P<company_id>\d+)/get-number/$', gather_user_phone_number, name='gather_user_phone_number'),
    url(r'^voice/(?P<company_id>\d+)/retry-getting-number/$',
        retry_gathering_user_phone_number,
        name='retry_gathering_user_phone_number'),
]
