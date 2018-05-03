from django.db import models
from django.conf import settings

class RequestManager(models.Manager):
  pass

# Create your models here.
class Request(models.Model):
  by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='outbox')
  
  to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='inbox')

  class Meta:
    unique_together = (('by', 'to'),)

  label = models.CharField(max_length=30, default='')
  message = models.CharField(max_length=70, default='')
  is_accepted = models.BooleanField(default=False)
  is_rejected = models.BooleanField(default=False)

  def accept(self):
    self.is_accepted = True
    self.save()

  def reject(self):
    self.is_rejected = False
    self.save()
