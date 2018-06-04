from django.db import models
from django.conf import settings 

from account.models import Profile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Activity(models.Model):
  USER_VISITED = 'v'

  ACTIVITY_TYPES = (
    (USER_VISITED,'user visited'),
  )

  profile = models.ForeignKey(Profile)
  activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
  date = models.DateTimeField(auto_now=True)

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()

  class Meta:
    unique_together = [('profile', 'activity_type', 'object_id'),]

