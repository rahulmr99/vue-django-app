from django.conf.urls import url

from .apps import RatingsManagerConfig
from .views import *

app_name = RatingsManagerConfig.name

urlpatterns = [
    url(r'^get/'
        r'(?P<token>.+)/'
        r'(?P<rating>[1-5])/$', GetFeedback.as_view(),
        name='get-feedback'),

    url(r'^thanks/$', ThanksView.as_view(), name='thank-you'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
]
