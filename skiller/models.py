from django.db import models
from django.conf import settings 
from .managers import SkillManager

from django.utils import timezone 

class SkillData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    skill = models.ForeignKey('Skill')

    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'skill'),)

    def __str__(self):
        return self.skill.codename

class Skill(models.Model):
    serial = models.AutoField(primary_key=True)
    
    codename = models.CharField(
        max_length=20,
        unique=True,
        help_text='codename for the skill')

    manager = SkillManager()

    def __str__(self):
        return self.codename

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('skill:create_skill')

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
