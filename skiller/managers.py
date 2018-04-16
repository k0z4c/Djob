from django.db import models 
from django.db import IntegrityError

from .exceptions import DuplicatedSkill 
from .helpers import _decorate_name

class SkillManager(models.Manager):

    def add(self, user, name): 
        codename = _decorate_name(name)
        from .models import SkillData
        (skill_data, created) = SkillData.objects.get_or_create(_codename=name)

        try:
            skill = self.create(user=user, data=skill_data)
        except IntegrityError:
            raise DuplicatedSkill 

        return skill

class ConfirmationManager(models.Manager):
    pass



