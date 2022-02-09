from django.core.exceptions import ValidationError


def validate_phone_number(number:str):
    if number and not (''.join([i for i in str(number) if i.isdigit()]).isdigit()):
        raise ValidationError(f'Invalid Phone Number : {number}')
