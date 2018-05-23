from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError
from .signals import(
  social_request_accepted, social_request_rejected
)

class RequestManager(models.Manager):
  def send_request(self, label, tile, by, to, ):
    try:
      req = self.create(label=label, tile=tile, by=by, to=to)
      return req
    except IntegrityError:
      pass


  def check_request(self, by, to):
    q = Q(by=by, to=to) | Q(by=to, to=by)
    return self.filter(q).exists()


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

  label = models.CharField(max_length=20)
  tile = models.CharField(max_length=70, default='')
  date = models.DateTimeField(auto_now_add=True)
  status_date = models.DateTimeField(auto_now=True)

  objects = RequestManager()

  class Meta:
    unique_together = (('by', 'to', 'label'),)
    
  # auto now maybe? 
  def accept(self):
    self.status = self.ACCEPTED
    self.save()

    print("sended")
    print(social_request_accepted.send_robust(sender=self.__class__, instance=self))

  def reject(self):
    self.status = self.REJECTED
    self.save()

    social_request_rejected.send(sender=self.__class__, instance=self)

  def get_absolute_url(self):
    from django.urls import reverse
    return reverse('marathon:manage_request', args=[self.pk,])
