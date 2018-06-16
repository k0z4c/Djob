from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from account.models import Profile
from django.contrib.postgres.fields import JSONField
from .signals import(
  social_request_accepted, social_request_rejected
)
from django.db import (
  models, IntegrityError
)


class RequestManager(models.Manager):
  def send_request(self, label, tile, by, to, data={}):
    try:
      req = self.create(label=label, tile=tile, by=by, to=to, data=data)
      return req
    except IntegrityError:
      pass

  def check_request(self, by, to):
    q = Q(by=by, to=to) | Q(by=to, to=by)
    return self.filter(q).exists()

class SocialRequest(models.Model):
  ACCEPTED = 'ACC'
  REJECTED = 'REJ'
  PENDING = 'PEN'
  DISABLED = 'DIS'
  REQUEST_STATUS_CHOICES = (
    (ACCEPTED, 'accepted'),
    (REJECTED, 'rejected'),
    (PENDING, 'pending'),
    (DISABLED, 'disabled'),
  )

  by = models.ForeignKey(
    Profile,
    related_name='marathon_sent')
  
  to = models.ForeignKey(
    Profile,
    related_name='marathon_received')

  status = models.CharField(
    choices=REQUEST_STATUS_CHOICES,
    default=PENDING,
    max_length=3
    )

  label = models.CharField(max_length=20)
  tile = models.CharField(max_length=200, default='', blank=True)
  date = models.DateTimeField(auto_now_add=True)
  status_date = models.DateTimeField(auto_now=True)
  data = JSONField(default=dict) 
  objects = RequestManager()

  class Meta:
    app_label = 'marathon'

  def accept(self):
    self.status = self.ACCEPTED
    self.save()

    social_request_accepted.send(sender=self.__class__, instance=self)

  def reject(self):
    self.status = self.REJECTED
    self.save()

    social_request_rejected.send(sender=self.__class__, instance=self)

  def get_absolute_url(self):
    return reverse('marathon:manage_request', args=[self.pk,])
