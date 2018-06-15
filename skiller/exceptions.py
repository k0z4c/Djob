from django.db import IntegrityError

class DuplicatedSkill(IntegrityError):
    pass 
