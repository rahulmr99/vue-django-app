from lexbot.tests.integration_tests.utils import LexBot


def book_new_appointment():
    """1. test booking new appointment """

    LexBot.say('book next monday 5 PM')

    # if this is the first time you are using ph then this question will be asked
    LexBot.if_replied('are you a new patient').say('yes')

    # if this is the first time
    LexBot.if_replied("What's your first and last name").say('Fname Lname')

    # if email id is not filled
    LexBot.if_replied('reply back with just your primary email address').say('jnoortheen@gmail.com')

    LexBot.replied('Your appointment is scheduled for ')


def reschedule_appointment():
    ### 2. test rescheduling appointment ###
    LexBot.say('reschedule').replied('I see you have an appointment on')
    LexBot.say('next Wednesday 5pm').replied('Thanks! Your appointment is scheduled for')


def cancel_appointment():
    ### 3. test cancelling appointment ###
    LexBot.say('cancel').replied('I see you have an appointment on')
    LexBot.say('yes').replied('your appointment is canceled')


if __name__ == '__main__':
    book_new_appointment()
    reschedule_appointment()
    cancel_appointment()
