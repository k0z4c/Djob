from django.db import models
from django.conf import settings 

# Create your models here.
class InviteRequest(models.Model):
  by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='invites_sended')
  to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='invites_received')

  class Meta:
    unique_together = (('by', 'to'),)

  date = models.DateTimeField(auto_now_add=True)

class ProjectPage(models.Model):
  users = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    through='InviteRequest'
    )
  owner = models.OneToOneField(settings.AUTH_USER_MODEL)

  name = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    return self.name
