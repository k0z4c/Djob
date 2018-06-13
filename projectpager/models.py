from django.db import models
from account.models import Profile

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

  name = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    return self.name

class Thread(models.Model):
  project = models.ForeignKey('ProjectPage', related_name='threads')
  created_by = models.ForeignKey(Profile)

  title = models.CharField(max_length=150)
  description = models.TextField()

  def __str__(self):
    return self.title

class Message(models.Model):
  discussion = models.ForeignKey('Thread', related_name='messages')
  posted_by = models.ForeignKey(Profile)

  body = models.TextField(default='')
  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.body
