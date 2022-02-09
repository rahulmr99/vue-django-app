from lexbot.tests.integration_tests.utils import LexBot
from .integration_test_bot_sms_scenario_1 import cancel_appointment

BREAK_TIME = "12:10 PM"


def book_on_breaking_hours_test_():
    """### 1. test booking new appointment ###"""
    LexBot.say(f'book day after tomorrow {BREAK_TIME}')

    # if this is the first time you are using ph then this question will be asked
    if 'are you a new patient' in str(LexBot.resp.content):
        LexBot.say('no')

    LexBot.replied('Our office is not open at that time, What time would you like to come in?')

    LexBot.say('no')

    # if this is the first time
    if f"What's your first and last name" in str(LexBot.resp.content):
        LexBot.say('Fname Lname')

    LexBot.replied('Your appointment is scheduled for 04:30 PM')


if __name__ == '__main__':
    book_on_breaking_hours_test_()
    cancel_appointment()
