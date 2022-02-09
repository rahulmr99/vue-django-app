"""use this file to test the zappa handler after it is packaged locally.
To create pacakge, run `fab test_dist`"""
import os
import sys

ZAPPA_DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')

if __name__ == '__main__':
    sys.path.insert(0, ZAPPA_DIST_DIR)
    os.environ['RUN_ENV'] = 'test_dist'

    from dist.handler import lambda_handler

    event = {
        u'currentIntent':
            {
                u'slots': {}, u'confirmationStatus': u'None', u'name': u'CancelAppointmentIntent',
                u'slotDetails': {}
            }, u'userId': u's1wo3xb7gv3ixrwcd3scpk58c678f1ve',
        u'bot': {u'alias': u'$LATEST', u'version': u'$LATEST', u'name': u'SMSBotRunTime'},
        u'inputTranscript': u'cancel', u'requestAttributes': None, u'invocationSource': u'DialogCodeHook',
        u'outputDialogMode': u'Text', u'messageVersion': u'1.0', u'sessionAttributes': {}
    }
    print(lambda_handler(event, {}))
