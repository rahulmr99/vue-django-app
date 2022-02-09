from lexbot.handlers import aws_connect
from lexbot.handlers.aws_connect import BOOK_APPOINTMENT, CANCEL_APPOINTMENT
from lexbot.msgs import NEW_USER_QUEST


def test_aws_connect_booking_handler(callerinfo_creator, aws_connect_flow_data):
    callerinfo_creator('1')
    data = aws_connect_flow_data(BOOK_APPOINTMENT)
    resp = aws_connect.handler(data, {})
    assert len(resp) == 5
    assert NEW_USER_QUEST in str(resp)


def test_aws_connect_cancel_handler(
        callerinfo_creator,
        next_monday_appointment,  # has appointment already
        aws_connect_flow_data,
):
    infoq = callerinfo_creator('3')
    assert infoq.want_cancelling
    # check booking
    data = aws_connect_flow_data(CANCEL_APPOINTMENT)
    resp = aws_connect.handler(data, {})
    assert len(resp) == 5
