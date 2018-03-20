from django.db import models
from django.conf import settings 
from .managers import SkillManager

from django.utils import timezone 

class Skill(models.Model):
    serial = models.AutoField(primary_key=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        )
    codename = models.CharField(
        max_length=20,
        unique=True,
        help_text='codename for the skill')

    manager = SkillManager()

    def __str__(self):
        return self.codename

class Confirmation(models.Model):
    to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='confirmations_by'
        )

    skill = models.ForeignKey(Skill)

    by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='confirmations_to'
        )

    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('to', 'skill', 'by'),)
