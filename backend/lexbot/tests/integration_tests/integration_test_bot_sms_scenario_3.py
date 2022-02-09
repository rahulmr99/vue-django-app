from .utils import LexBot
from .integration_test_bot_sms_scenario_1 import cancel_appointment


def book_new_appointment():
    """try to book at unavailable time"""

    LexBot.say(f'book next monday 4:26 PM')

    # if this is the first time you are using ph then this question will be asked
    LexBot.if_replied('are you a new patient').say('yes')

    LexBot.replied('that time is not available. Does ')

    LexBot.say('yes', )

    # if this is the first time
    LexBot.if_replied("What's your first and last name").say('Fname Lname')
    # if email id is not filled
    LexBot.if_replied('reply back with just your primary email address').say('jnoortheen@gmail.com')

    LexBot.replied('Your appointment is scheduled for ')


if __name__ == '__main__':
    book_new_appointment()
    cancel_appointment()
