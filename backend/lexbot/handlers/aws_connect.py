import logging
from typing import Union

from django.utils.functional import cached_property
from raven_python_lambda import RavenLambdaWrapper

from lexbot.helpers.request_mappers import AppointmentHandler
from lexbot.models import CallerInfoQueue

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

BOOK_APPOINTMENT = 'BookAppointment'
CANCEL_APPOINTMENT = 'CancelAppointment'
RESCHEDULE_APPOINTMENT = 'RescheduleAppointment'


class ConnectContactData(object):
    def __init__(self, data: dict):
        self.data = data or {}

    @property
    def customer_number(self) -> Union[str, None]:
        return self.data['CustomerEndpoint']['Address'] if self.data else None


class ContactFlowEventHandler(object):
    @classmethod
    def handler(cls, event: dict, context: dict) -> dict:
        eventhandler = cls(event, context)
        return eventhandler.run()

    def __init__(self, event: dict, context: dict):
        self.event = event
        self.conext = context
        self.contact_data = ConnectContactData(event['Details'].get('ContactData'))

    @property
    def invokeFunction(self):
        return self.event['Details']['Parameters']['InvokeFunction']

    @cached_property
    def callerinfo(self):
        return CallerInfoQueue.get_caller_info(self.contact_data.customer_number)

    def run(self) -> dict:
        appointmenthandler = AppointmentHandler(
            company_id=self.callerinfo.generalsettings_id,
            callerPhoneNumber=self.callerinfo.caller_number,
            callerCountry=self.callerinfo.caller_country,
            providerPhoneNumber=self.callerinfo.provider_number,
        )

        message = None
        if self.invokeFunction == CANCEL_APPOINTMENT:
            # aws connect will play this message
            message = appointmenthandler.get_customer_confirmation_for_cancel()
        elif self.invokeFunction == BOOK_APPOINTMENT:
            if appointmenthandler.customer_account:
                message = appointmenthandler.get_msg_for_booking_date()
            else:
                message = appointmenthandler.get_msg_for_new_patient()
        elif self.invokeFunction == RESCHEDULE_APPOINTMENT:
            if appointmenthandler.customer_account:
                message = appointmenthandler.get_msg_for_reschedule_date()
            else:
                message = appointmenthandler.get_msg_for_new_patient()

        if message is None:
            raise NotImplementedError

        return {
            'callerPhoneNumber': appointmenthandler.callerPhoneNumber,
            'callerCountry': appointmenthandler.callerCountry,
            'providerPhoneNumber': appointmenthandler.providerPhoneNumber,
            'company_id': appointmenthandler.company_id,
            'message': message,
        }


@RavenLambdaWrapper()
def handler(event, context):
    """top level function to be called from importer libs"""
    logger.debug(f'Called from contact flow {event} {context}', )

    return ContactFlowEventHandler.handler(event, context)
