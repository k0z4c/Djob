from django.core.validators import RegexValidator

def validate_invalid_chars(value):
    import string
    import re
    char_blacklist = string.punctuation
    regex = re.compile('^[^{}]$'.format(char_blacklist))
    RegexValidator(
        regex=regex,
        message='{} characters are not accepted'.format(char_blacklist),
    )(value)
