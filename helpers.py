from django.db import IntegrityError

class CodenameError(IntegrityError):
  pass

def _decorate_name(name):
  if not isinstance(name, str):
    raise CodenameError
  words = name.lower().split()
  codename = '_'.join(words)

  return codename

def get_decorated_name(decorated_name):
  words = decorated_name.split('_')
  return ' '.join(words)
