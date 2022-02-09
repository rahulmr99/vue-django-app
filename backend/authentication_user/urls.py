from django.conf.urls import url
from . import views
from .apps import AuthenticationUserConfig

app_name = AuthenticationUserConfig.name

urlpatterns = [
    url('^oauth2callback/$', views.auth_return),
    url('^test/$', views.index),
]
