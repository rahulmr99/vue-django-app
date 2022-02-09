# from collections import OrderedDict

# import datetime

# from authentication_user.models import Account, CustomerAccount
# from calendar_manager.models import CalendarDb
# from lexbot.handlers.sms import schedule
# from lexbot.handlers.sms.schedule import TIME_FMT
# from lexbot.handlers.utils import filter_time_slots
# from lexbot.msgs import CHOOSE_ANOTHER_DAY


# def test_filter_time_slots():
#     times = [datetime.datetime.now() + datetime.timedelta(minutes=i * 10) for i in range(20)]
#     slots = OrderedDict([(time.strftime(TIME_FMT), time) for time in times])
#     res = filter_time_slots(slots)
#     assert len(res) == 3


# def test_schedule_book(db, root_user, next_monday, mailoutbox, lexbot_book, twilio_post_data):
#     # step 0: asks user type
#     lexbot_book.intend(intent_name=schedule.BOOK_INTENT).replied('*are you a new patient*')

#     # step 1: asks for date if not fully inferred time
#     lexbot_book.say_yes().replied('What day would you like to come in*')

#     # step 2: asks for AP time
#     lexbot_book.say(
#         Date=next_monday
#     ).replied('What time would you like to come that day?*')

#     # step 3: asks for time
#     lexbot_book.say(
#         Time='15:05'
#     ).replied("*I'm sorry, that time is not available. Does 3:10 PM work instead?*")

#     # step 3: asks for next suggested time
#     lexbot_book.say_no().replied('*OK, please choose another time that day. We have 3:20 PM, 3:50 PM, 4:20 PM*')

#     # step 3-1: show next available time
#     lexbot_book.say(
#         Time='15:20'
#     ).replied("*What's your first and last name?*")

#     # step 5: finally book appointment
#     lexbot_book.say(
#         FirstName='FName LName'
#     ).replied('*Your appointment is scheduled for 3:20 PM on*')

#     CalendarDb.objects.update()  # clear cached count
#     assert CalendarDb.objects.count() == 1


# def test_schedule_book_with_time_given(db, root_user, mailoutbox, lexbot_book, twilio_post_data, next_monday):
#     assert CustomerAccount.objects.filter().count() == 0

#     lexbot_book.call(
#         intent_name=schedule.BOOK_INTENT,
#         slots={
#             'Date': next_monday,
#             'Time': '16:00'
#         }).replied('*are you a new patient*')

#     # step 1: ask for name since other slots are filled
#     lexbot_book.say_yes().replied("What's your first and last name")

#     # step 5: finally book appointment
#     lexbot_book.say(FirstName='FName LName').replied('Your appointment is scheduled for 4:00 PM on')

#     CalendarDb.objects.update()  # clear cached count
#     assert CalendarDb.objects.count() == 1


# def test_schedule_book_on_closed_day(db, root_user: Account, next_sunday, mailoutbox, twilio_post_data, lexbot_book, ):
#     """try to book when that day is not available"""
#     # prepare data
#     assert CustomerAccount.objects.filter().count() == 0

#     lexbot_book.call(
#         intent_name=schedule.BOOK_INTENT,
#         slots={
#             'Date': next_sunday,
#             'Time': '16:00',
#         }).replied('*are you a new patient*')

#     lexbot_book.say_yes().replied("our office is closed that day")


# def test_schedule_book_on_break_hour(
#         db, root_user: Account, twilio_post_data, mailoutbox, lexbot_book, next_monday
# ):
#     """try to book when that day is not available"""
#     assert CustomerAccount.objects.count() == 0

#     # step 0: ask user type
#     lexbot_book.call(
#         intent_name=schedule.BOOK_INTENT,
#         slots={
#             'Date': next_monday,
#             'Time': '12:10',
#         }).replied('*are you a new patient*')

#     lexbot_book.say_yes().replied("office is not open at that time, What time would you like to come")


# def test_schedule_book_choose_another_day(
#         db, root_user: Account, twilio_post_data, lexbot_book, mailoutbox, next_monday
# ):
#     """try to book when that day is not available"""
#     assert CustomerAccount.objects.count() == 0
#     lexbot_book.call(
#         intent_name=schedule.BOOK_INTENT,
#         slots={
#             'Date': next_monday,
#             'Time': '10:05',
#         }).replied('*are you a new patient*')

#     # step 1: ask for name since other slots are filled
#     lexbot_book.say_yes().replied("I'm sorry, that time is not available. Does")

#     lexbot_book.say_no().replied('* please choose another time that day. *say "choose another day"*')

#     lexbot_book.say(input='Another day').replied(CHOOSE_ANOTHER_DAY)
