TEST_TWILIO_MSG_DATA = {
    'ToCountry': 'US',
    'ToState': '',
    'SmsMessageSid': 'SM6e278d660c9943727ac2141bb285a006',
    'NumMedia': '0',
    'ToCity': '',
    'FromZip': '56470',
    'SmsSid': 'SM6e278d660c9943727ac2141bb285a006',
    'FromState': 'MN',
    'SmsStatus': 'received',
    'FromCity': 'PARK RAPIDS',
    'Body': 'message content',
    'FromCountry': 'US',
    'To': '+18559972901',
    'ToZip': '',
    'NumSegments': '1',
    'MessageSid': 'SM6e278d660c9943727ac2141bb285a006',
    'AccountSid': 'AC4b33ce4f86f272fb4045df8a110c0047',
    'From': '+12184141141',
    'ApiVersion': '2010-04-01'
}

LEX_EVENT = {
    'messageVersion': '1.0', 'invocationSource': 'DialogCodeHook', 'userId': '12184141141',
    'sessionAttributes': {},  # all values must be string
    'requestAttributes': {},
    'bot': {'name': 'SMSBotRunTime', 'alias': '$LATEST', 'version': '$LATEST'},
    'outputDialogMode': 'Text',
    'currentIntent': {'name': 'SMSBot',
                      'slots': {'Choose': None, 'APTime': None, 'FirstName': None, 'Time': None,
                                'Date': None},
                      'slotDetails': {'Choose': {'resolutions': [], 'originalValue': None},
                                      'APTime': {'resolutions': [], 'originalValue': None},
                                      'FirstName': {'resolutions': [], 'originalValue': None},
                                      'Time': {'resolutions': [], 'originalValue': None},
                                      'Date': {'resolutions': [], 'originalValue': None}},
                      'confirmationStatus': 'None'},
    'inputTranscript': 'book'
}

LEX_RESP = {
    'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                         'content-length': '331',
                                         'content-type': 'application/json',
                                         'date': 'Fri, 09 Feb 2018 20:11:16 GMT',
                                         'x-amzn-requestid': '602f2f10-0dd5-11e8-8603-e16f268dd7b7'},
                         'HTTPStatusCode': 200,
                         'RequestId': '602f2f10-0dd5-11e8-8603-e16f268dd7b7',
                         'RetryAttempts': 0},
    'dialogState': 'Fulfilled',
    'intentName': 'SMSBot',
    'message': "I'm sorry. I can't find your appointment from the phone number you called in. Have a wonderful day.",
    'sessionAttributes': {},
    'slots': {'APTime': None,
              'Choose': None,
              'Date': None,
              'FirstName': None,
              'Time': None}
}

AWS_CONTACTFLOW_EVENT = {
    'Details': {
        'ContactData': {
            'Attributes': {}, 'Channel': 'VOICE', 'ContactId': '818c669e-95d4-4e5e-8750-2fff887a17f3',
            'CustomerEndpoint': {
                'Address': TEST_TWILIO_MSG_DATA['From'], 'Type': 'TELEPHONE_NUMBER'
            },
            'InitialContactId': '818c669e-95d4-4e5e-8750-2fff887a17f3', 'InitiationMethod': 'INBOUND',
            'InstanceARN': 'arn:aws:connect:us-east-1:029992932068:instance/e7f9f1cf-2fc6-4055-bc22-6967ed18fd90',
            'PreviousContactId': '818c669e-95d4-4e5e-8750-2fff887a17f3', 'Queue': None,
            'SystemEndpoint': {'Address': '+17029847578', 'Type': 'TELEPHONE_NUMBER'}
        },
        'Parameters': {}
    },
    'Name': 'ContactFlowEvent'
}
