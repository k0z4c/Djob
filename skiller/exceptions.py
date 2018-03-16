from django.db import IntegrityError

class SkillExists(IntegrityError):
    pass

class CodenameError(IntegrityError):
    pass
    