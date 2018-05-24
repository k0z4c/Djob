from django.db import models
from django.conf import settings 

from account.models import Profile
# here we have to instantiated Project page before create an Invite request
# Create your models here.
class InviteRequest(models.Model):
  by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='invites_sended')
  to = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='invites_received')

  project_page = models.OneToOneField('ProjectPage')

  class Meta:
    unique_together = (('by', 'to'),)

  date = models.DateTimeField(auto_now_add=True)

class ProjectPage(models.Model):
  profiles = models.ManyToManyField(
    Profile,
    related_name = 'projectpages')

  owner = models.ForeignKey(
    Profile,
    related_name='+')

  name = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    return self.name
