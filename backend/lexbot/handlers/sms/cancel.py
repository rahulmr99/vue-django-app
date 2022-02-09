import logging

from raven_python_lambda import RavenLambdaWrapper

from lexbot.helpers.request_mappers import LexHandler
from lexbot.helpers.response_mappers import *
from ... import msgs

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

CANCEL_INTENT = 'CancelAppointmentIntent'
UNCONFIRM_CANCEL_FROM_VOICE_INTENT = 'UnconfirmCancelAppointment'
CONFIRM_CANCEL_FROM_VOICE_INTENT = 'ConfirmCancelAppointmentIntent'


class CancelAppointmentHandler(LexHandler):
    intents = {CANCEL_INTENT, UNCONFIRM_CANCEL_FROM_VOICE_INTENT, CONFIRM_CANCEL_FROM_VOICE_INTENT, }

    def get_closemsg(self) -> str:
        if self.check_appointment_cancel_action():
            return self.check_appointment_cancel_action()

        # case 3: in case this is the second time we are receving after confirmation
        elif self.intent.name == CONFIRM_CANCEL_FROM_VOICE_INTENT or self.intent.is_confirmed:
            # use this session attribute to delete the appointment
            self.calendar_appointment.cancel_appointment()
            return msgs.APPOINTMENT_CANCELLED

        # case 3.1: in case it is denied
        elif self.intent.name == UNCONFIRM_CANCEL_FROM_VOICE_INTENT or self.intent.is_denied:
            return msgs.CANELLATION_DENIED

    def run(self) -> dict:
        closemsg = self.get_closemsg()
        if closemsg:
            return close_fullfilled(self.attrs, closemsg)

        # case 4: show the appointment details to the user and confirm whether they want to cancel the appointment
        return confirm_intent(
            self.attrs, self.intent.name, self.intent.slots, self.get_customer_confirmation_for_cancel(), None
        )


@RavenLambdaWrapper()
def handler(event, context):
    """top level function to be called from importer libs"""
    return CancelAppointmentHandler.handler(event, context)
