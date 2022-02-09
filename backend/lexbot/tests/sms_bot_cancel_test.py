# from calendar_manager.models import CalendarDb


# def test_cancel_appointment(
#         db, next_monday_appointment, phone_customer, root_user, mailoutbox, twilio_post_data, lexbot_cancel,
# ):

#     # test prepared date
#     assert CalendarDb.objects.filter().active_appointments().count() == 1

#     # use lex to cancel that appointment
#     # step 1: confirm delete
#     lexbot_cancel.intend(intent_name='CancelAppointmentIntent').replied('Alright. Would you like to reschedule now?')

#     # step 2: delete appointment
#     lexbot_cancel.say_yes().replied('Alright. Would you like to reschedule now?')

#     CalendarDb.objects.update()  # clear cached count
#     assert CalendarDb.objects.filter().active_appointments().count() == 0
#     assert len(mailoutbox) == 4
