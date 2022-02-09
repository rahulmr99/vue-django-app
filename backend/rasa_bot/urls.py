from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^sms/user/$', rasa_bot_user, name='rasa_bot_user'),
    url(r'^sms/check-timeslot-available/$', check_timeslot_available, name='check_timeslot_available'),
    url(r'^sms/book-appt/$', rasa_bot_book_appt, name='rasa_bot_book_appt'),
    url(r'^sms/reschedule-appt/$', reschedule_appt, name='reschedule_appt'),
    url(r'^sms/cancel-appt/$', cancel_appt, name='cancel_appt'),
    url(r'^chat/get-token/$', generate_access_token, name='generate_access_token'),
    url(r'^chat/get-token-bot/$', generate_access_token_bot, name='generate_access_token_bot'),
    url(r'^sms/user/get-provider-email/$', get_provider_email, name='get_provider_email'),
    url(r'^sms/user/get-upcoming-appointments/(?P<phone_no>\d+)/$', get_upcoming_appts, name='get_upcoming_appts'),
    url(r'^sms/user/send-sms/$', send_sms_to_user, name='send_sms_to_user'),
    url(r'^sms/user/add-member-to-channel/$', add_member_to_channel, name='add_member_to_channel'),
    url(r'^get-provider-timezone/(?P<provider_number>.*)/$', get_provider_timezone, name='get_provider_timezone'),
    url(r'^on-off-ai/$', toggle_ai, name='toggle_ai'),
    url(r'^ai-on-off-status/(?P<phone_no>\d+)/$', get_ai_on_off_status, name='get_ai_on_off_status'),
    url(r'^email/$', send_fallback_email, name='send_fallback_email'),
    url(r'^get-provider-phone-number/$',get_provider_phone_number,name='get_provider_phone_number'),
    url(r'^check-phone-no-is-valid/$', check_phone_number_is_valid, name='check_phone_number_is_valid'),
    url(r'^get-pre-booking-date/$', get_pre_booking_date, name='get_pre_booking_date'),
]