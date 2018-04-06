from django.db import models
from django.conf import settings 
from .managers import SkillManager, ConfirmationManager

from django.utils import timezone 

class Skill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    data = models.ForeignKey(
        'SkillData',
        on_delete=models.CASCADE
        )

    date = models.DateTimeField(default=timezone.now)

    objects = SkillManager()

    class Meta:
        unique_together = (('user', 'data'),)

    def __str__(self):
        return self.data.codename

class Confirmation(models.Model):
 
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
        )

    # recursive relationship
    by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='confirmed_to',
        )

    to = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='confirmed_by',
        )

    date = models.DateTimeField(default=timezone.now)

    objects = ConfirmationManager()

    class Meta:
        unique_together = (('skill', 'to', 'by'),)

class SkillData(models.Model):
    serial = models.AutoField(primary_key=True)  
    codename = models.CharField(
        max_length=20,
        unique=True,
        help_text='codename for the skill'
        )

    def __str__(self):
        return self.codename

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('skill:create_skill')


