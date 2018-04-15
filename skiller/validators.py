from django.core.exceptions import ValidationError

def validate_chars(input):
    import string
    bad_chars = string.digits + string.whitespace + string.punctuation 
    is_bad_char = lambda c: c in bad_chars
    
    invalid_chars = [ char for char in input if is_bad_char(char) ]
    if invalid_chars: 
        raise ValidationError(
                'Please remove these bad chars: %(invalid)s',
                params={'invalid': invalid_chars}
            )
