from django.db import models
from django.conf import settings 

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Activity(models.Model):
  FRIEND_ADDED = 'f'
  CONFIRMATION = 'c'
  ACTIVITY_TYPES = (
    (FRIEND_ADDED,'friend added'),
    (CONFIRMATION , 'confirmation received' ),
  )

  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
  date = models.DateTimeField(auto_now_add=True)

  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
