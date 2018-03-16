from django.db import models
from django.conf import settings 
from .managers import SkillManager

class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    serial = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=50, unique=True, help_text='codename for the skill')

    confirmations = models.IntegerField(default=0)
    manager = SkillManager()

    def __str__(self):
        return self.codename


