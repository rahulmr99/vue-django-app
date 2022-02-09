import logging

from raven_python_lambda import RavenLambdaWrapper

from .forward_new_user import NewUserAppoitnmentHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

NEW_PATIENT_INTENT = 'ForwardReturningUser'


class ReturningUserAppoitnmentHandler(NewUserAppoitnmentHandler):
    intents = {NEW_PATIENT_INTENT}

    def __init__(self, *args):
        super().__init__(*args)
        self.ReturningUser = 1  # returning user


@RavenLambdaWrapper()
def handler(event, context):
    """top level function to be called from importer libs"""
    return ReturningUserAppoitnmentHandler.handler(event, context)
