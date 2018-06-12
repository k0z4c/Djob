from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
def validate_invalid_chars(value):
    import string
    import re
    char_blacklist = string.punctuation
    for c in char_blacklist:
      if c in value:
        raise ValidationError(message='please, remove bad chars %(chars)s', params={'chars': char_blacklist}, code='invalid')
    # RegexValidator(regex=re.compile('^\w*$'), message='only alphanumeric chars are allowed', code='invalid', inverse_match=True)
    #  la validazione occhio a c/c++; sexondo me non c'e' molta validazione da fare...