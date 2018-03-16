from django.db import models
from django.conf import settings 

class Skill(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    serial = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=50, help='codename for the skill')

    confirmations = models.IntgerField(default=0)
    manager = SkillManager()

    def __str__(self):
        return self.codename


