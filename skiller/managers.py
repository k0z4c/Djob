from django.db import models 
from .exceptions import SkillExists, CodenameError, DuplicatedSkill 
from django.db import IntegrityError 

class SkillManager(models.Manager):

    def add_skill(self, user, name): 
        # same as try:... except..
        codename = self._decorate_name(name)
        from .models import SkillData
        (skill_data, created) = SkillData.objects.get_or_create(codename=codename)

        try:
            skill = self.create(user=user, data=skill_data)
        except IntegrityError:
            raise DuplicatedSkill 

        return skill

    # helper method 
    def _decorate_name(self, skill_name):
        if not isinstance(skill_name, str):
            raise CodenameError
        words = skill_name.split()
        # check and remove bad chrs 
        codename = '_'.join(words)

        return codename

# this might be useful 
class ConfirmationManager(models.Manager):
    pass



