from django.conf.urls import url
from .views import (RegisterView, SubscriptionView, FetchSubscriptionView, CancelSubscriptionView, StatusSubscription,
                    ReactivateSubscription, )

app_name = 'billing'
urlpatterns = [
    url('^register/$', RegisterView.as_view(), name='register'),
    url('^subscribe/$', SubscriptionView.as_view(), name='subscribe'),
    url('^fetch-subscription/(?P<account_id>\d+)/$', FetchSubscriptionView.as_view(), name='fetch_subscription'),
    url('^cancel-subscription/$', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    url('^status-subscription/$', StatusSubscription.as_view(), name='status_subscription'),
    url('^reactivate-subscription/$', ReactivateSubscription.as_view(), name='reactivate_subscription'),
]
