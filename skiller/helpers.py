from .exceptions import CodenameError

def _decorate_name(name):
        if not isinstance(name, str):
            raise CodenameError
        words = name.lower().split()
        codename = '_'.join(words)

        return codename
