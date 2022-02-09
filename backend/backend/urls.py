"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django_ses.views import handle_bounce
# from graphene_django.views import GraphQLView
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from app_settings.views import redirect_to_s3_view
from authentication_user.viewsets import RegisterView, EmailConfirmationCode

API_TITLE = 'API Easy Appointments'
API_DESCRIPTION = '...'

urlpatterns = [
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # ============================== App views ===================================
    url(r'^embedded/', include('embed_page.urls')),
    url(r'^feedback/', include('ratings_manager.urls', namespace='feedback', )),
    url(r'^mailer/', include('mailer.urls', namespace='mailer')),
    # =======================================  Actions  =====================================
    url(r'^auth/', include('authentication_user.urls', namespace='auth')),
    url(r'^icalendar/$', RegisterView.as_view(), name='icalendar'),
    # =======================================  Login  =======================================
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^send-reset-link/$', EmailConfirmationCode.as_view(), name='send_reset_link'),
    url(r'^login/$', obtain_jwt_token, name='login_token'),
    url(r'^token_check/$', verify_jwt_token, name='token_check'),
    # =======================================  API v1  ======================================
    url(r'^api/v1/', include('api_v1.urls', namespace='api_v1')),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # =======================================    DOC   ======================================
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),

    # to handle AWS SES subscriptions
    url(r'^ses/bounce/$', csrf_exempt(handle_bounce)),
    # a dashboard to see send reports
    url(r'^admin/email-dashboard/', include('django_ses.urls')),
    # handle twilio IVR
    url(r'^ivrs/', include('openvbx.urls')),
    # handle AWS lex bot integration with twilio and AWS connect
    url(r'^bot/', include('lexbot.urls', namespace='bot')),
    url(r'^rasa-bot/', include('rasa_bot.urls', namespace='rasa-bot')),
    url(r'^billing/', include('billing.urls', namespace='billing')),
]

if os.environ.get('SERVERTYPE') == 'AWS Lambda':
    urlpatterns.append(
        url(r'^static/(?P<asset_path>.+)', redirect_to_s3_view),
    )
