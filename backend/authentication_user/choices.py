from utils_plus.choices import ChoicesEnum


class MAIL_STATUS(ChoicesEnum):
    subscribed = 'Subscribed'
    unsubscribed = 'Un-Subscribed'
    bounced = 'Email Bounced and unlisted'
    complained = 'Complained and unlisted'
