from lexbot.tests.integration_tests.utils import setup_django, LexBot

setup_django()


def book_new_appointment():
    """try to book at unavailable time"""

    LexBot.say(f'book next monday 4:26 PM')

    # if this is the first time you are using ph then this question will be asked
    LexBot.if_replied('are you a new patient').say('yes')

    LexBot.replied('that time is not available. Does ')

    LexBot.say('no').replied('To choose another day say just say "choose another day"')

    LexBot.say('Another day').replied('What day would you like to come in? Just say day and time with')


if __name__ == '__main__':
    book_new_appointment()
