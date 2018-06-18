from django.db import models
from account.models import Profile
from helpers import _decorate_name, get_decorated_name

class ProjectPage(models.Model):
  profiles = models.ManyToManyField(
    Profile,
    related_name = 'projectpages')

  class Meta:
    permissions = (
      ('can_open_threads', 'Can open a thread'),
    )
    
  owner = models.ForeignKey(
    Profile,
    related_name='+')

  _name = models.CharField(max_length=50)

  description = models.TextField()

  @property
  def name(self):
      return get_decorated_name(self._name)

  @name.setter
  def name(self):
    return _decorate_name(self._name)
  
  def __str__(self):
    return get_decorated_name(self._name)

class Thread(models.Model):
  project = models.ForeignKey('ProjectPage', related_name='threads')
  created_by = models.ForeignKey(Profile)

  title = models.CharField(max_length=150)
  description = models.TextField()

class Message(models.Model):
  discussion = models.ForeignKey('Thread', related_name='messages')
  posted_by = models.ForeignKey(Profile)

  body = models.TextField(default='')
  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.body
