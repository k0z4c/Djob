from django.db import models
from django.conf import settings
from django.utils import timezone

from .signals import(
  social_request_accepted, social_request_rejected
)

class RequestManager(models.Manager):
  pass

# Create your models here.
class SocialRequest(models.Model):
  ACCEPTED = 'ACC'
  REJECTED = 'REJ'
  PENDING = 'PEN'
  REQUEST_STATUS_CHOICES = (
    (ACCEPTED, 'accepted'),
    (REJECTED, 'rejected'),
    (PENDING, 'pending'),
  )

  by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='marathon_sent')
  
  to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='marathon_received')

  status = models.CharField(
    choices=REQUEST_STATUS_CHOICES,
    default=PENDING,
    max_length=3
    )

  label = models.CharField(unique=True, max_length=20, default='')
  tile = models.CharField(max_length=70, default='')
  date = models.DateTimeField(auto_now_add=True)
  status_date = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = (('by', 'to'),)

  # auto now maybe? 
  def accept(self):
    self.status = ACCEPTED
    self.save()

    social_request_accepted.send(sender=self.__class__)

  def reject(self):
    self.status = REJECTED
    self.save()

    social_request_rejected.send(sender=self.__class__)
