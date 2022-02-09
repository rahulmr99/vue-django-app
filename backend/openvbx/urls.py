from django.conf.urls import url

from .apps import OpenvbxConfig
from . import views, viewsets

app_name = OpenvbxConfig.name

urlpatterns = [
    url(r'^voice/$', views.twiml_voice_handler, name='call-client'),
    url(r'^token/(?P<company_id>\d+)/$', viewsets.GetTokenAPI.as_view(), name='get-token'),
    url(r'^caller-vr/(?P<company_id>\d+)/$', views.caller_voice_response_view, name='call_responder_view'),
    url(r'^record/(?P<company_id>\d+)/$', views.record_call_view, name='record_call_view'),
    url(r'^get_twilio_number/$', viewsets.GetIsTwilioNumberPresent.as_view(), name='get_twilio_number'),
    url(r'^record/(?P<company_id>\d+)/endcallback$', views.handle_recording_view, name='handle_recording_view'),
    url(r'^get_numbers/', viewsets.GetPhoneNumbers.as_view(), name='get_numbers'),
]
