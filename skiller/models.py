from django.db import models
from django.conf import settings
from django.utils import timezone 
from account.models import Profile
from .managers import (
    SkillManager, ConfirmationManager
    )

from .validators import validate_invalid_chars
from .helpers import _decorate_name

class Skill(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
        )
    data = models.ForeignKey(
        'SkillData',
        on_delete=models.CASCADE
        )

    description = models.TextField(
        max_length=400,
        blank=True,
        help_text='Describe your eventual experience or let blank')
    date = models.DateTimeField(default=timezone.now)

    objects = SkillManager()

    class Meta:
        unique_together = (('profile', 'data'),)

    def __str__(self):
        return self.data.codename

class Confirmation(models.Model):
 
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
        )

    # recursive relationship
    by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='confirmed_to',
        )

    to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='confirmed_by',
        )

    date = models.DateTimeField(default=timezone.now)

    objects = ConfirmationManager()

    class Meta:
        unique_together = (('skill', 'to', 'by'),)

class SkillData(models.Model):
    serial = models.AutoField(primary_key=True) 
    _codename = models.CharField(
        db_column='skill name',
        max_length=20,
        unique=True,
        validators = [validate_invalid_chars,],
        help_text='codename for the skill',
        )

    @property
    def codename(self):
        return self._codename

    @codename.setter
    def codename(self, value):
        self._codename = _decorate_name(value)

    def __str__(self):
        return self.codename

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('skill:add_skill')


