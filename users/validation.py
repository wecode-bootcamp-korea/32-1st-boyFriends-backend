from django.core.exceptions import ValidationError
import re

def validate_email(email):
    EMAIL_REGEX = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError("EMAIL_INVALIDATION")

def validate_password(password):
    PASSWORD_REGEX = '^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    if not re.match(PASSWORD_REGEX, password):
        raise ValidationError("PASSWORD_INVALIDATION")