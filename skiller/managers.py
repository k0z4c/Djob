from django.db import models 
from .exceptions import SkillExists, CodenameError 

class SkillManager(models.Manager):
    def create_skill(self, user, name):
        codename = self._decorate_name(name) 

        qs = self.filter(user=user, codename=codename)
        if qs.exists():
            raise SkillExists
        skill = self.create(codename=codename)
        user.skill_set.add(skill)
        return skill 


    def _decorate_name(self, skill_name):
        if not isinstance(skill_name, str):
            raise CodenameError
        words = skill_name.split()
        # check and remove bad chrs 
        codename = '_'.join(words)

        return codename
