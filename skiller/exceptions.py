from django.db import IntegrityError

class CodenameError(IntegrityError):
    pass

class DuplicatedSkill(IntegrityError):
    pass 
