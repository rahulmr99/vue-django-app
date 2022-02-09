from django.conf.urls import url

from . import views
from .apps import MailerConfig

app_name = MailerConfig.name

urlpatterns = [
    url(r'^unsubscribe/(?P<mailid_encoded>[\w-]+.[\w-]+)/confirm/$', views.ConfirmUnsubscribeView.as_view(),
        name='confirm-unsubscribe'),
    url(r'^unsubscribe/(?P<mailid_encoded>[\w-]+.[\w-]+)/done/$', views.ShowUnsubscribedView.as_view(),
        name='notify-unsubscribed'),
]
