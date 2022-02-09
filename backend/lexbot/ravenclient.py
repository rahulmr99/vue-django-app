from raven.contrib.awslambda import LambdaClient

raven_client = LambdaClient()


def exception_handler(e, event, context):
    raven_client.captureException(exc_info=e, data=dict(event=event, context=context))
    return True
