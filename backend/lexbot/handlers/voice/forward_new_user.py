import logging

from raven_python_lambda import RavenLambdaWrapper

from lexbot.handlers.sms.schedule import AppointmentSlotsMixin

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

NEW_PATIENT_INTENT = 'ForwardNewUserIntent'


class NewUserAppoitnmentHandler(AppointmentSlotsMixin):
    intents = {NEW_PATIENT_INTENT}

    def __init__(self, *args):
        super().__init__(*args)
        self.ReturningUser = 0  # new user

    def run(self) -> dict:
        # forward to booking intent with returning user set to false
        return self.fill_date_slot()


@RavenLambdaWrapper()
def handler(event, context):
    """top level function to be called from importer libs"""
    return NewUserAppoitnmentHandler.handler(event, context)
