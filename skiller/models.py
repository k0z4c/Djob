from django.db import models
from django.conf import settings 
from exceptions import SkillExists, CodenameError 

class SkillManager(models.Manager):
    def insert_skill(self, user, name):
        codename = self._decorate_name(name) 

        qs = self.filter(user=user, codename=codename)
        if qs.exists()
            raise SkillExists
        return self.create(user=user, codename=codename)


    def _decorate_name(self, skill_name):
        if not isinstance(skill_name, str):
            raise CodenameError
        words = skill_name.split()
        codename = '_'.join(words)

        return codename

class Skill(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    serial = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=50, help='codename for the skill')

    confirmations = models.IntgerField(default=0)
    manager = SkillManager()

    def __str__(self):
        return self.codename


