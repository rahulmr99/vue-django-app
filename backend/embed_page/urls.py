from django.conf.urls import url

from .apps import EmbedPageConfig
from .views import *

app_name = EmbedPageConfig.name
urlpatterns = [
    url('^(?P<company_id>[0-9]+)/$', EmbeddableBookingPage.as_view(), name='company_embed_book_id'),
    url('^(?P<company_slug>[\w-]+)/$', EmbeddableBookingPage.as_view(), name='company_embed_book_slug'),
    url('script/(?P<company_id>[0-9]+)/$', EmbeddableScript.as_view(), name='embedder_js'),

    # embeddable popup script
    url('script/popup/(?P<client_id>[0-9]+)/$', EmbeddablePopupScript.as_view(), name='site_embedder_js'),
    url('page/popup/index.html', embeddable_popup_page, name='site_embedder_page'),
    url('json/popup/(?P<general_setting_id>[0-9]+)/$', embeddable_popup_json, name='site_embedder_json'),
]
