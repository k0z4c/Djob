from django.db import models
from account.models import Profile 
from django.db import IntegrityError

class FriendshipManager(models.Manager):
  def create_friendship(self, **kwargs):
    by = kwargs.get('by')
    to = kwargs.get('to')

    if by.pk == to.pk:
      raise IntegrityError

    self.create(by=by, to=to)
    self.create(by=to, to=by)

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

