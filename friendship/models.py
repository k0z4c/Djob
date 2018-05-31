from django.db import models
from account.models import Profile 

class FriendshipManager(models.Manager):
  def create_friendship(self, **kwargs):
    self.create(by=kwargs.get('by'), to=kwargs.get('to'))
    self.create(by=kwargs.get('to'), to=kwargs.get('by'))

  def are_friends(self, profile1, profile2):
    qs = profile1.contacts.filter(to=profile2)
    return qs.exists()

class Friendship(models.Model):
  by = models.ForeignKey(Profile, related_name='contacts')
  to = models.ForeignKey(Profile, related_name='+')

  date = models.DateTimeField(auto_now_add=True)
  objects = FriendshipManager()

  def __str__(self):
    return self.to.user.email

